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
    - Run the application with Gradio by executing the following command:

        python gradio-chat.py

    - Run the application with Chainlit by executing the following command:

        chainlit run chainlit-chat.py -w

    After executing the command, Gradio will start the application and automatically open it in your default web browser.
    If it doesn't open automatically, Gradio will provide a local URL in the terminal output, which you can manually copy and paste into your browser to access the application.

Happy processing!

-------------
Usefully commands
-------------
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



#conda install faiss-gpu
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 faiss-cpu scrapy -c pytorch -c nvidia -c conda-forge
#conda install -c nvidia cuda-toolkit
pip install --upgrade pip setuptools
pip install gradio chainlit sentence-transformers ragatouille dspy-ai

¿Cómo funciona el proceso de preinscripción para el Grado en Turismo y cuáles son las tasas de matrícula para diferentes inscripciones?


=================
Ubuntu 20.04
sudo apt-get update
sudo apt-get install build-essential

mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh

RELOAD terminal

git clone https://github.com/levnikolaevich/chat-bot-aitana.git
cd chat-bot-aitana

conda create --name AitanaENV
conda activate AitanaENV

conda config --show

conda config --add channels pytorch
conda config --add channels nvidia
conda config --add channels conda-forge
#conda config --add channels pytorch/label/nightly

#conda env create -f environment.yaml

conda install faiss-gpu
conda install pytorch torchvision torchaudio pytorch-cuda -c pytorch -c nvidia
conda install -c nvidia cuda-toolkit
conda install scrapy
pip install gradio
pip install chainlit
pip install sentence-transformers
pip install ragatouille
pip install dspy-ai


pip install gdown
mkdir -p ./data/ckpt

gdown --id 13rNSmQI_VaMtwlMBSUaxEGybzJEl5KTi -O ./data/ckpt/ckpt_sifu.zip
ls ./data/ckpt




nvcc --version
nvidia-smi


===========

wsl --unregister Ubuntu
wsl --unregister Ubuntu-20.04
