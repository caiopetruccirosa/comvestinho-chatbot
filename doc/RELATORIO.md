# Relatório de desenvolvimento

Este relatório busca descrever o processo de exploração das bibliotecas e ferramentas utilizadas, como o LangChain e o StreamLit, assim como a implementação do chat bot ComvestinhoChatBot e a avaliação do assistente conversacional.

## Exploração

A etapa de exploração teve como objetivo entender como construir um assistente conversacional baseado em **Retrieval Augmented Generation** (**RAG**). Para isso, foram realizadas diversas buscas na **engine** de busca do Google como "how to build RAG based models" ou "build a chatbot based on RAG".

Assim, considerando os resultados encontrados e as informações passadas pelo Slack do processo seletivo, foi encontrada a biblioteca **LangChain** e a partir daí o estudo se deu principalmente pela documentação da ferramenta, em conjunto com alguns vídeos encontrados no YouTube, como o [Retrieval-Augmented Generation (RAG) using LangChain and Pinecone - The RAG Special Episode](https://www.youtube.com/watch?v=J_tCD_J6w3s&ab_channel=GenerativeAIonAWS) do canal **Generative AI on AWS**.

Por fim, para o deployment da aplicação como um todo foi estudado a ferramenta **StreamLit**, por conta citação feita via Slack.

Assim, as principais páginas que foram estudadas foram as seguintes:

- [Retrieval-augmented generation (RAG)](https://python.langchain.com/docs/use_cases/question_answering/);
- [Document loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/);
- [Document loaders: Integrations](https://python.langchain.com/docs/integrations/document_loaders/);
- [Remembering chat history](https://python.langchain.com/docs/use_cases/question_answering/chat_vector_db);
- [Vector store-backed retriever](https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore);
- [Chatbots](https://python.langchain.com/docs/use_cases/chatbots);
- [Using a Retriever](https://python.langchain.com/docs/use_cases/question_answering/vector_db_qa);
- [What Chunk Size and Chunk Overlap Should You Use?](https://dev.to/peterabel/what-chunk-size-and-chunk-overlap-should-you-use-4338);
- [A Comprehensive Guide to Using Chains in Langchain](https://www.analyticsvidhya.com/blog/2023/10/a-comprehensive-guide-to-using-chains-in-langchain/);
- [Using OpenAI functions](https://python.langchain.com/docs/modules/chains/how_to/openai_functions);
- [Create an app](https://docs.streamlit.io/library/get-started/create-an-app);
- [Build conversational apps](https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps);
- [Deploy your app](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Models](https://platform.openai.com/docs/models/models);
- [Embeddings](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings).

Vale indicar que, para implementação do assistente, foi utilizado o Jupyter Notebook como ferramenta para entender e experimentar as funcionalidades disponibilizadas pelas bibliotecas, assim como para prototipar e debuggar o código desenvolvido.

## Implementação

### ComvestinhoChatBot object

Para implementação de um ChatBot baseado em **RAG**, foi levantado a necessidade de determinar as seguintes etapas, conforme a página [Retrieval-augmented generation (RAG)](https://python.langchain.com/docs/use_cases/question_answering/): 
Etapas:

>
> 1. Loading: First we need to load our data. Use the LangChain integration hub to browse the full set of loaders.
> 2. Splitting: Text splitters break Documents into splits of specified size
> 3. Storage: Storage (e.g., often a vectorstore) will house and often embed the splits
> 4. Retrieval: The app retrieves splits from storage (e.g., often with similar embeddings to the input question)
> 5. Generation: An LLM produces an answer using a prompt that includes the question and the retrieved data
>

Para a etapa de __loading__, foi utilizado o **AsyncHtmlLoader** e o **Html2TextTransformer**, que possibilitou baixar a página HTML da Resolução GR-031/2023, de 13/07/2023. Foi considerado utilizar o objeto **WebBaseLoader** para esta finalidade, porém o texto da página ficou com alguns erros de formatação.Já para a etapa de __splitting__, foi utilizado o **RecursiveCharacterTextSplitter** e foram experimentados alguns valores para os parâmetros __chunk_size__ e __chunk_overlap__ e acabaram influenciando bastante o resultado final, o que não foi uma grande surpresa dado que o tamanho dos __chunks__ de texto influencia diretamente a quantidade de "documentos" diferentes que poderão ser colocados no prompt do Chat Bot, devido à limitação de tokens da API da OpenAI. Assim, para a etapa de __storage__, foi utilizado o ChromaDB, que armazenou __embeddings__ de cada __chunk__ de texto gerados a partir do modelo `text-embedding-ada-002` da OpenAI. 

As etapas de __retrieval__ e __generation__ são etapas que são executadas mais frequentemente, já que são realizadas a cada mensagem nova do usuário na conversa com o assistente. Então, o __retrieval__ realizado foi relativamente simples, sendo apenas um match de similaridade de cosseno do __embedding__ da pergunta usuário com os documentos no __storage__. Para o __generation__, foi criado um template de prompt, que insere as informações de histórico de mensagens do chat e as informações de contexto recuperadas na etapa de __retrieval__.

Durante o processo de implementação e exploração, foi investigado o uso de algumas __chain__ da biblioteca **LangChain**, como a **ConversationalRetrievalChain** e **RetrievalQA**, porém a implementação que se mostrou mais satisfatória e flexível foi a composta pela construção dos prompts e o __retrieval__ de documentos de forma explícita.

Vale ressaltar também que, para utilização dos modelos da OpenAI via API foi necessário criar uma conta na plataforma da OpenAI e gerar uma `OPENAI_API_KEY`. Além disso, para facilitar a geração dos __embeddings__ do texto da Resolução do Vestibular da Unicamp, foi depositado 5 USD de crédito para realizar o upgrade do tier da conta usada de Free para Tier 1 e aumentar **Rate Limit** por minuto de tokens da API. Isso foi feito pois gerar os __embeddings__ dos documentos em um único batch ultrapassava **Rate Limit** disponível para uma conta Free Tier.

### Aplicação conversacional baseada em StreamLit

Para a construção da aplicação de Chat, foi utilizado o [StreamLit](https://streamlit.io/). 

O código da aplicação foi baseado no tutorial [Build conversational apps](https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps). Já o deployment, foi realizado conforme o tutorial [Deploy your app](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app), que faz deploy da aplicação a partir do repositório hospeado no GitHub. Assim, bastou utilizado o SDK disponível para Python, definir as dependências para o projeto no arquivo `requirements.txt` e adicionar a `OPENAI_API_KEY` como uma __secret__ do projeto no dashboard de deploy.

A aplicação publicada pode ser acessada através do seguinte link: [ComvestinhoChatBot](https://comvestinhochatbot.streamlit.app).

## Avaliação

Por fim, a avaliação do modelo foi feita de maneira relativamente simples.

Utilizando a ferramenta ChatGPT, foram geradas 50 perguntas que estudantes poderiam ter sobre o Vestibular da Unicamp, a partir do seguinte prompt:

> Você pode criar uma série de 50 perguntas possíveis que estudantes possam fazer sobre o Vestibular da Unicamp, como "Quais são os cursos possíveis para me inscrever" ou "Quantas vagas existem para o curso X"?

As 50 perguntas geradas foram armazenadas no arquivo TXT [questions.txt](./data/questions.txt). Então, a fim de avaliar o assistente conversacional, foi feito um [script](./app/answer_questions.py) para perguntar cada uma das perguntas ao modelo, armazenando a resposta em um outro arquivo TXT [answers.txt](./data/answers.txt), com cada pergunta precendendo a resposta dada.

Analisando manualmente as perguntas e as respostas dadas, pode-se ver que o modelo conseguiu capturar boa parte do conhecimento relacionado ao Vestibular da Unicamp, dando respostas satisfatórias para perguntas como as perguntas 10, 11 e 12. Porém, ficou notável algumas dificuldades que o assistente teve para responder perguntas relacionadas à quantidade de vagas ou aos cursos disponíveis, como as perguntas 2 e 27. Na minha análise, a maior dificuldade de responder estas perguntas está relacionada à dificuldade de recuperar estes conhecimentos nos documentos cujo __retrieval__ foi realizado, pois, devido à formatação das tabelas e outras partes da página baixada, o texto com os conhecimentos necessários para responder estas perguntas não ficou "amigável" para a interface de prompt utilizada em um assistente baseado em **RAG**.