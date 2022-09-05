# Youtube Comment Deleter

Created a program to remove YouTube scam comments stating that you have won a prize and to cover shipping expenses on Telegram or Whatsapp. 


## Extracting comments from Youtube via channel id. 

```
python3 youtube.py --channel_id channelId --n number_of_videos
```

## Label Data 

Label all of the spam comments saved in the youtube_data directory to TRUE. All of the comments are by default false. 

<img width="337" alt="image" src="https://user-images.githubusercontent.com/35375203/188513691-a3e1e33e-cffc-4462-b550-d4725914824f.png">

## Convert labeled data to BIO format

```
python3 convert_bio.py --input_file data_dir --output_dir model_input_location
```

## Train model 

```
python3 main.py --task youtube --model_dir youtube_model do_train = True do_eval = True
```

## Delete comments (Run evaluation) 

```
python3 delete_comments.py --model_dir youtube_model --channel_id channelID --use_channel_id True
python3 delete_comments.py --model_dir youtube_model --video_id videoID --use_channel_id False
```

> Using the channel id will retrived the latest video in the specified channel. 

## References

- [Huggingface Transformers](https://github.com/huggingface/transformers)
- [pytorch-crf](https://github.com/kmkurn/pytorch-crf)
