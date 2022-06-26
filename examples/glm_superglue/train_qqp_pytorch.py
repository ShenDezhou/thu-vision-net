# Education Purpose Only.
#
# Licensed under the Apache License, Version 2.0 (the "License")

from flagai.trainer import Trainer
from flagai.model.glm_model import GLMForSingleTokenCloze
from flagai.model.bert_model import BertForClsClassifier
from flagai.data.tokenizer import GLM10bENBPETokenizer, GLMLargeEnWordPieceTokenizer
from flagai.metrics import accuracy_metric
from flagai.data.dataset import SuperGlueDataset
from flagai.test_utils import CollateArguments



task_name = 'qqp'
trainer = Trainer(env_type='pytorch',
                  pytorch_device='cuda',
                  epochs=2,
                  batch_size=128+256,
                  eval_interval=500,
                  log_interval=10,
                  save_interval=1e5,
                  lr=1e-5,
                  weight_decay=0.1,
                  checkpoint_activations=True,
                  gradient_accumulation_steps=10,
                  fp16=True,
                  warm_up=0.1,
                  save_dir="./glm_large_qqp_pytorch")

model = GLMForSingleTokenCloze.from_pretrain(download_path="/mnt/test_10b_models",
                                             model_name="GLM-large-en")

#tokenizer = GLM10bENBPETokenizer()
tokenizer = GLMLargeEnWordPieceTokenizer()

train_dataset = SuperGlueDataset(task_name=task_name,
                                 data_dir='./datasets/',
                                 dataset_type='train',
                                 tokenizer=tokenizer,
                                 cloze_eval=True)
valid_dataset = SuperGlueDataset(task_name=task_name,
                                 data_dir='./datasets/',
                                 dataset_type='dev',
                                 tokenizer=tokenizer,
                                 cloze_eval=True)
cl_args = CollateArguments()
cl_args.cloze_eval = True
if task_name in ['copa', 'wsc', 'record']:
    cl_args.multi_token = True

from flagai.data.dataset import ConstructSuperglueStrategy

collate_fn = ConstructSuperglueStrategy(cl_args,
                                        tokenizer,
                                        task_name=task_name)
trainer.train(model,
              train_dataset=train_dataset,
              valid_dataset=valid_dataset,
              collate_fn=collate_fn,
              metric_methods=[["acc", accuracy_metric]])
