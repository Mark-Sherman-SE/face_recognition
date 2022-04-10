import torch
from torchvision import datasets
from nn.models.inception_resnet_v1 import InceptionResnetV1
from torch.utils.tensorboard import SummaryWriter
from nn.models.utils import training
from nn.utils import get_test_transform, get_train_transform
import os


def retrain(batch_size=8, num_epochs=25, children_to_unfreeze=5, data_dir="nn/data/aligned", name="weights"):
    data_transforms = {
        'train': get_train_transform(),
        'test': get_test_transform(),
    }
    #data_dir = 'data/aligned'

    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                              data_transforms[x])
                      for x in ['train', 'test']}

    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x],
                                                  batch_size=batch_size,
                                                  shuffle=True)
                   for x in ['train', 'test']}

    classes = image_datasets['train'].classes
    device = "cuda" if torch.cuda.is_available() else "cpu"

    resnet = InceptionResnetV1(classify=True, pretrained='vggface2', num_classes=len(classes)).to(device)

    num_of_children = len(list(resnet.children()))
    for i, child in enumerate(resnet.children()):
        if i < num_of_children - children_to_unfreeze:
            for param in child.parameters():
                param.requires_grad = False

    optimizer = torch.optim.Adam(resnet.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, [4, 8, 12])

    loss_fn = torch.nn.CrossEntropyLoss()
    metrics = {
        'fps': training.BatchTimer(),
        'acc': training.accuracy
    }
    writer = SummaryWriter()
    writer.iteration, writer.interval = 0, 10

    print('\n\nInitial')
    print('-' * 10)
    resnet.eval()
    test_loss, test_metric = training.pass_epoch(
        resnet, loss_fn, dataloaders["test"],
        batch_metrics=metrics, show_running=True, device=device,
        writer=writer
    )

    print("Test_loss", test_loss)
    print("Test_metric", test_metric)

    for epoch in range(num_epochs):
        print('\nEpoch {}/{}'.format(epoch + 1, num_epochs))
        print('-' * 10)

        resnet.train()
        train_loss, train_metric = training.pass_epoch(
            resnet, loss_fn, dataloaders["train"], optimizer, scheduler,
            batch_metrics=metrics, show_running=True, device=device,
            writer=writer
        )

        resnet.eval()
        test_loss, test_metric = training.pass_epoch(
            resnet, loss_fn, dataloaders["test"],
            batch_metrics=metrics, show_running=True, device=device,
            writer=writer
        )
    torch.save(resnet.state_dict(), f"../result/weights/{name}.pth")
    writer.close()
