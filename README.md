# Personal RAG

This is a very simple RAG project. It was made as a Weekend project to learn a little about Generative AI, Chatbots and document search.

> Disclaimer: There are many places where the code can be improved and many functionalities that could be added.
> There are also things that just where not completely implemented (like adding files to a store.)

## Spinning the system up

You should first open **LM-Studio** and start a server there. You can choose the model you want to use for completions by setting the environment variable *model* and the embedding model by setting *embed_model*

In a terminal, you can simply run the following command from the root directory of the project:

```bash
    cd back && fastapi run main.py
```

And then you can spin up the front end by running:

```bash
    cd catalofFront && npm install && npm run dev
```


## Contributing or using the code

Anyone is free to contribute to this project or simply use the code for whatever purpose the may want to use it.
