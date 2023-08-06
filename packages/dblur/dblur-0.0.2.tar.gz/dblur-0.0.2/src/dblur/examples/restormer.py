from trainers.restormer import RestormerTrainer
from testers.restormer import RestormerTester


def default_train(checkpoint_save_name, train_img_dir, val_img_dir=None, batch_size=64, epochs=2000,
                  save_checkpoint_freq=100, val_freq=100):
    """ Trains a Restormer model on the given training dataset with the default
    parameters mentioned in the paper "Restormer: Efficient Transformer for 
    High-Resolution Image Restoration"

    Args:
        train_img_dir: directory of training data
        val_img_dir: directory of validation data
        checkpoint_save_name: name of checkpoint (includes model, optimizer, 
            lr_scheduler) to be saved at a given frequency. 
        batch_size: batch size for training. Default value set to 64 as in the 
            paper.
        epochs: number of epochs for training.
        save_checkpoint_freq: frequency at which checkpoint is saved.
        val_freq: frequency at which validation is performed. 
    """

    restormer_trainer = RestormerTrainer()
    train_dataloader = restormer_trainer.get_train_dataloader(train_img_dir, batch_size=batch_size)
    if val_img_dir is not None:
        val_dataloader = restormer_trainer.get_val_dataloader(val_img_dir, batch_size=batch_size)
    else:
        val_dataloader = None

    model = restormer_trainer.get_model()
    optimizer = restormer_trainer.get_optimizer(model.parameters())
    loss_func = restormer_trainer.get_loss()
    lr_scheduler = restormer_trainer.get_lr_scheduler(optimizer)
    restormer_trainer.train(model,
                            train_dataloader,
                            val_dataloader,
                            optimizer,
                            loss_func,
                            save_checkpoint_freq=save_checkpoint_freq,
                            logs_folder='runs',
                            checkpoint_save_name=checkpoint_save_name,
                            val_freq=val_freq, write_logs=True,
                            lr_scheduler=lr_scheduler,
                            epochs=epochs)


def default_test(model_path, test_img_dir, is_checkpoint=True, batch_size=64):
    """ Tests a Restormer model on the given testing dataset with the default
    parameters mentioned in the paper "Restormer: Efficient Transformer for 
    High-Resolution Image Restoration".
    
    Args:
        model_path: path of the checkpoint (model, optimizer and lr_scheduler) 
            or just the model.
        test_img_dir: directory of testing data.
        is_checkpoint: specifies if path specified in model_path is a 
            checkpoint (model, optimizer and lr_scheduler) or just a model.
        batch_size: batch size for testing.
    """

    restormer_tester = RestormerTester()
    test_dataloader = restormer_tester.get_test_dataloader(test_img_dir, batch_size=batch_size)
    model = restormer_tester.get_model()
    loss_func = restormer_tester.get_loss()
    restormer_tester.test(model,
                          model_path,
                          test_dataloader,
                          loss_func,
                          is_checkpoint=is_checkpoint,
                          window_slicing=False)
