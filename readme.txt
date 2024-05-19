Project Setup Instructions
==========================

Welcome to our project! Follow these setup instructions to ensure everything runs smoothly.

Prerequisites
-------------

Before you start, make sure you have the following prerequisites installed and set up on your system:

1. Setting Up the Conda Environment
    For package and environment management, this project utilizes Conda. If Conda is not yet installed on your system, it is recommended to install Miniconda. It's a minimal installer for Conda and provides all necessary tools.

    - **Installing Miniconda:**

      1. Download Miniconda for Windows, macOS, or Linux from the official website: https://docs.conda.io/en/latest/miniconda.html.
      2. Follow the provided instructions to install Miniconda. Optionally, add Miniconda to your PATH during installation or use the Miniconda prompt/terminal for Conda commands.
      3. For Windows execute: setx PATH "%PATH%;C:\ProgramData\miniconda3;C:\ProgramData\miniconda3\Scripts;C:\ProgramData\miniconda3\Library\bin" /M

    - **Setting Up Your Project Environment with Conda:**

      1. Open your system's command prompt or terminal.
      2. Change directory to your project's root folder where the `environment.yml` file is located.
         ```
         cd /path/to/your/project
         ```
      3. Create the Conda environment using the `environment.yml` file by running:
         ```
         conda env create -f environment.yml
         ```
         This command sets up a new Conda environment with all the dependencies specified in the `environment.yml` file.
      4. Once the environment creation process is complete, activate the new environment with:
         ```
         conda activate AitanaENV
         ```
      5. To verify the setup, check the installed packages in the environment:
         ```
         conda list
         ```

    This process will ensure that you have a Conda environment ready with all the necessary dependencies for the project. Make sure to activate the project-specific Conda environment whenever you work on the project to maintain consistency across development and production setups.

2. Verifying Compiler Command Availability and Setting Up the Compiler (for the RAGatouille Module in Windows 11)
   To compile C++ code that ragatouille depends on, you need the MSVC (Microsoft Visual C++) compiler, which is available through Visual Studio Community Edition.

    1. Download and install Visual Studio Community Edition from the official website: https://visualstudio.microsoft.com/downloads/.
    2. During installation, select the "Desktop development with C++" workload to ensure the C++ compiler and relevant tools are installed.
    3. Ensure that the path to the MSVC compiler is added to your system's PATH environment variable.
        C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\<version>\bin\Hostx64\x64

    To confirm that the compiler is correctly set up and accessible from your Conda environment, you can perform a simple check using the command prompt.

    Open the command prompt and activate your Conda environment:
         ```
         conda activate AitanaENV
         ```
    Check if the cl command is accessible by running:
         ```
         cl
         ```

    If the command returns a version, it confirms that the compiler is set up correctly.

By following these setup instructions, you'll ensure that all components of the project function correctly.

-------------
Crawling a Website
-------------
To crawl a website, you will use Scrapy from the terminal.
Ensure you are in the project directory where scrapy.cfg file is located.

Follow these simple steps to initiate the crawl:
- Open a terminal or Anaconda Prompt and navigate to your project directory.
- Activate your environment with:
     ```
     conda activate AitanaENV
     ```
- Initiate the crawling process with Scrapy by executing the following command:

    scrapy crawl aitana_spider

Once executed, Scrapy will begin crawling the website as defined by the aitana_spider. The process involves requesting pages, parsing the returned HTML to extract data, and optionally following links to other pages to continue the crawl.

-------------
Launching the Application
-------------

    To start the application, you need to execute it using Gradio from the terminal.
    Make sure you are in the project directory where your main.py file is located.

    Then, follow these steps to launch the application:
    - Open a terminal or Anaconda Prompt and navigate to your project directory.

    - Activate your environment with:
         ```
         conda activate AitanaENV
         ```

    - Set up the Hugging Face credentials by running and following the instructions in the terminal:
         ```
         huggingface-cli login
         ```

    - Run the application with Chainlit by executing the following command:

        chainlit run chainlit-chat.py -w

    After executing the command, Gradio will start the application and automatically open it in your default web browser.
    If it doesn't open automatically, Gradio will provide a local URL in the terminal output, which you can manually copy and paste into your browser to access the application.

Happy processing!

-------------
Usefully commands
-------------
WINDOWS 11
    conda create --name AitanaENV
    conda activate AitanaENV
    conda deactivate
    conda remove --name AitanaENV --all

    conda env export > environment.yml
    conda env create -f environment.yml
    conda env update --name AitanaENV --file environment.yml --prune

    conda list --export > package-list.txt
    conda update --all
    conda clean --all
    pip list --outdated | Select-String -Pattern "^\w+" | ForEach-Object { $_.Matches.Groups[0].Value } | ForEach-Object { pip install --upgrade $_ }
    pip cache purge


    conda install pytorch torchvision torchaudio pytorch-cuda=12.1 faiss-cpu scrapy -c pytorch -c nvidia -c conda-forge
    pip install --upgrade pip setuptools
    pip install gradio chainlit sentence-transformers ragatouille dspy-ai

¿Cómo funciona el proceso de preinscripción para el Grado en Turismo y cuáles son las tasas de matrícula para diferentes inscripciones?


=================
Ubuntu 20.04
    sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt-get install libtiff5 build-essential -y

    mkdir -p ~/miniconda3 && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh && \
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 && \
    rm -rf ~/miniconda3/miniconda.sh && \
    ~/miniconda3/bin/conda init bash && \
    ~/miniconda3/bin/conda init zsh

RELOAD terminal

    git clone https://github.com/levnikolaevich/chat-bot-aitana.git
    cd chat-bot-aitana

Variant 1:
    conda create --name AitanaENV
    conda activate AitanaENV
    conda env update --name AitanaENV --file environment-ubuntu.yml --prune

Variant 2:
    conda env create -f environment-ubuntu.yml
    conda activate AitanaENV

For clean system:
    conda create --name AitanaENV
    conda activate AitanaENV
    conda install faiss-gpu pytorch torchvision torchaudio pytorch-cuda=12.1 cuda-toolkit scrapy -c pytorch -c nvidia -c conda-forge
    pip install gradio chainlit sentence-transformers ragatouille dspy-ai huggingface_hub accelerate
    conda env export > environment-ubuntu.yml

nvcc --version
nvidia-smi


===========

wsl --unregister Ubuntu-20.04

\\wsl$


docker login

docker build -t levnikolaevich87/chat-bot-aitana:latest .
docker push levnikolaevich87/chat-bot-aitana:latest
docker pull levnikolaevich87/chat-bot-aitana:latest

docker run -p 8080:8000levnikolaevich87/chat-bot-aitana:latest
docker run -e HF_TOKEN='your token' --gpus all -p 8080:8000 levnikolaevich87/chat-bot-aitana:latest



docker images
docker tag chat-bot-aitana levnikolaevich87/chat-bot-aitana:latest

