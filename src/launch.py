import os

os.system("python set_up.py")
os.system("python upload_files.py")
os.system("python install_hadoop.py")
os.system("python install_spark.py")
os.system("python launch_experiments.py")
os.system("python process_results.py")
os.system("python menu.py")