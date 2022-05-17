# %%
from utils import example_eval_config, example_train_config, train_model, eval_model

# %% [markdown]
# # 1: Gender

# %%
# train_config = {
#     'model_name_or_path': 'facebook/wav2vec2-large-slavic-voxpopuli-v2',
#     'TASK': 'NEW_GENDER_2s',
#     'NUM_EPOCH': 2,
#     'data_files': {
#         'train': '001_gender_train.csv',
#         'validation': '001_gender_dev.csv'
#         },
#     "clip_seconds": 2,
#     "output_column": "Speaker_gender"
# }

# OUTPUT_DIR = train_model(train_config)


# %%
results = []


# %%

for clip in [-1, 2]:
    train_config = {
        'model_name_or_path': 'facebook/wav2vec2-large-slavic-voxpopuli-v2',
        'TASK': 'NEW_GENDER_2s' if clip==2 else "NEW_GENDER",
        'NUM_EPOCH': 2,
        'data_files': {
            'train': '001_gender_train.csv',
            'validation': '001_gender_dev.csv'
            },
        "clip_seconds": clip,
        "output_column": "Speaker_gender"
    }

    OUTPUT_DIR = train_model(train_config)

    for split in "dev test".split():
        config = {
            "output_column": "Speaker_gender",
            "model_name_or_path": OUTPUT_DIR+"/checkpoint-250",
            "eval_file": f"001_gender_{split}.csv",
            "clip_seconds": clip,
            "train_config": train_config
        }
        y_true, y_pred = eval_model(config)

        results.append({**config, "y_true": y_true, "y_pred": y_pred})


import pandas as pd
df = pd.DataFrame(data=results)
df.to_json("008_results.jsonl", origin="records", lines=True)
# %% [markdown]
# # 2: speaker ID

# %%

for clip in [-1, 2]:
    train_config = {
        'model_name_or_path': 'facebook/wav2vec2-large-slavic-voxpopuli-v2',
        'TASK': 'NEW_SPEAKER_ID_2s' if clip==2 else "NEW_SPEAKER_ID",
        'NUM_EPOCH': 2,
        'data_files': {
            'train': '003_speaker_id_train_for_datasets.csv',
            'validation': '003_speaker_id_test_for_datasets.csv'
            },
        "clip_seconds": clip,
        "output_column": "Speaker_name"
    }

    OUTPUT_DIR = train_model(train_config)

    for split in "dev test".split():
        config = {
            "output_column": "Speaker_name",
            "model_name_or_path": OUTPUT_DIR+"/checkpoint-1250",
            "eval_file": f"003_speaker_id_{split}_for_datasets.csv",
            "clip_seconds": clip,
            "train_config": train_config,
        }
        y_true, y_pred = eval_model(config)

        results.append({**config, "y_true": y_true, "y_pred": y_pred})

# %%
import pandas as pd
df = pd.DataFrame(data=results)
df.to_json("008_results.jsonl", origin="records", lines=True)

# %% [markdown]
# # 3. Age group - males

# %%

for clip in [-1]:
    train_config = {
        'model_name_or_path': 'facebook/wav2vec2-large-slavic-voxpopuli-v2',
        'TASK': 'NEW_AGE_ID_2s' if clip==2 else "NEW_AGE_ID",
        'NUM_EPOCH': 15,
        'data_files': {
            'train': '006_age_train.csv',
            'validation': '006_age_test.csv'
            },
        "clip_seconds": clip,
        "output_column": "Speaker_age_group"
    }

    OUTPUT_DIR = train_model(train_config)
    
    for split in "dev test".split():
        config = {
            "output_column": "Speaker_age_group",
            "model_name_or_path": OUTPUT_DIR+"/checkpoint-2250",
            "eval_file": f"006_age_{split}.csv",
            "clip_seconds": clip,
            "train_config": train_config,
        }
        y_true, y_pred = eval_model(config)

        results.append({**config, "y_true": y_true, "y_pred": y_pred})

# %%
import pandas as pd
df = pd.DataFrame(data=results)
df.to_json("008_results.jsonl", origin="records", lines=True)

# %%



