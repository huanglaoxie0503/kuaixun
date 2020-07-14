```markdown
1.证券时报网 
 快讯:http://kuaixun.stcn.com/index.shtml

2.部署位置：jlch@10.10.15.246:/home/jlch/LinuxSpider/kuaixun

3.存储路径：kuaixun@crawl@10.10.15.105

4.运行机制：5分钟运行一次

*/1 6-23 * * * cd /home/jlch/LinuxSpider/kuaixun && ./run.py
*/50 0-5 * * * cd /home/jlch/LinuxSpider/kuaixun && ./run.py

```


