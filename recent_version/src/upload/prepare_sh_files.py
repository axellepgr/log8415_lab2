import os

os.system("sed -i -e 's/\\r$//' pg4300_hadoop.sh")
os.system("chmod +x pg4300_hadoop.sh")

os.system("sed -i -e 's/\\r$//' pg4300_linux.sh")
os.system("chmod +x pg4300_linux.sh")

os.system("sed -i -e 's/\\r$//' experiment_hadoop.sh")
os.system("chmod +x experiment_hadoop.sh")

os.system("sed -i -e 's/\\r$//' experiment_spark.sh")
os.system("chmod +x experiment_spark.sh")

os.system("sed -i -e 's/\\r$//' generate_times_file.sh")
os.system("chmod +x generate_times_file.sh")
