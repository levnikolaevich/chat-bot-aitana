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

        python main.py

    After executing the command, Gradio will start the application and automatically open it in your default web browser.
    If it doesn't open automatically, Gradio will provide a local URL in the terminal output, which you can manually copy and paste into your browser to access the application.

Happy processing!

-------------
Flight Log
-------------
Usefully commands:
conda deactivate
conda remove --name AitanaENV --all

conda env export > environment.yml
conda env create -f environment.yml
conda env update --name AitanaENV --file environment.yml

pip install faiss-cpu
pip install sentence-transformers
pip install gradio