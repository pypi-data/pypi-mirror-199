#!/usr/bin/env python
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class BinaryClassificationFF(nn.Module):
    def __init__(self, n_features: int):
        super(BinaryClassificationFF, self).__init__()
        self.fc1 = nn.Linear(n_features, math.ceil(n_features*2/5))
        self.dropout = nn.Dropout(p=0.2)
        self.fc2 = nn.Linear(math.ceil(n_features*2/5), math.ceil(n_features*1/5))
        self.fc3 = nn.Linear(math.ceil(n_features*1/5), math.ceil(n_features*1/10))
        self.fc4 = nn.Linear(math.ceil(n_features*1/10), 2)

    def forward(self, x):
        x = self.dropout(F.relu(self.fc1(x)))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.log_softmax(self.fc4(x), dim=1)
        return x

    def _distributed_training(self, 
                              train_data, 
                              batch_size, 
                              criterion, 
                              optimizer, 
                              epochs, 
                              print_freq, 
                              logger, 
                              **kwargs):
        # retrieve if cuda is available
        # set device
        
        device = torch.device("cuda", local_rank)
        # get PyTorch environment variables
        if "WORLD_SIZE" in os.environ: 
            world_size = int(os.environ["WORLD_SIZE"])
        if "RANK" in os.environ:
            rank = int(os.environ["RANK"])
        if "LOCAL_RANK" in os.environ:
            local_rank = int(os.environ["LOCAL_RANK"])
        # initialize distributed process group using default env:// method
        torch.distributed.init_process_group(backend="nccl")
        train_sampler = torch.utils.data.distributed.DistributedSampler(train_data)
        # train set 
        trainloader = torch.utils.data.DataLoader(
                train_data, 
                batch_size=batch_size, 
                shuffle=(train_sampler is None), 
                sampler=train_sampler
            )
        model = self.to(device)
        # setup parallel data apparatus
        model = nn.parallel.DistributedDataParallel(
            model, device_ids=[local_rank], output_device=local_rank
        )
        # define loss function and optimizer
        for e in range(epochs):
            running_loss = 0.0
            for i, data in enumerate(trainloader, 0):
                # set data to device
                inputs, labels = data[0].to(device), data[1].to(device)
                # zero gradients with optimizer
                optimizer.zero_grad()
                # get predictions
                log_ps = model(inputs)
                loss = criterion(log_ps, labels)
                # run backward
                loss.backward()
                optimizer.step()
                # add loss to running loss
                running_loss += loss.item()
                if i % print_freq == 0:  # print every print_freq mini-batches
                    print(
                        "Rank %d: [%d, %5d] loss: %.3f"
                        % (rank, e + 1, i + 1, running_loss / print_freq)
                    )
                    running_loss = 0.0

        print(f"Rank {rank}: Finished Training.")
        # if rank==0:
            # log model when completed
        return None
    
    def train(
        self, 
        train_data,
        criterion, 
        optimizer, 
        epochs,
        logger,
        distributed: bool=False, 
        batch_size: int=64, 
        print_freq: int=100
    ):
        if distributed:
            # pass local arguments of train function to distributed training
            self._distributed_training(
                **locals()
            )
        else:
            # retrieve if cuda is available
            # set device
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            
            # train set loader and set device to model
            trainloader = torch.utils.data.DataLoader(
                    train_data, 
                    batch_size=batch_size, 
                    shuffle=True
                )
            model = self.to(device)
            # define loss function and optimizer
            for e in range(epochs):
                running_loss = 0.0
                for i, data in enumerate(trainloader, 0):
                    # set data to device
                    inputs, labels = data[0].to(device), data[1].to(device)
                    # zero gradients with optimizer
                    optimizer.zero_grad()
                    # get predictions
                    log_ps = model(inputs)
                    loss = criterion(log_ps, labels)
                    # run backward
                    loss.backward()
                    optimizer.step()
                    # add loss to running loss
                    running_loss += loss.item()
                    # log running loss
                    logger.info(f"Running loss: {running_loss}")
                else:
                    logger.info(f"Training loss: {running_loss/len(trainloader)}")

