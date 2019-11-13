rm -rf connect_projects_old/
mv connect_projects/ connect_projects_old/
connect shell find /local-scratch/jiafulow/connect-client/ -name "jftest*" -type d -exec rm -rf {} +
python example.py

cd connect_projects/jftest1 && connnode && cd -
cd connect_projects/jftest2 && connnode && cd -
