# DeepFM-FPS-Estimator

This is a Final Year Project of Teesside University produced by Long Yau.

This project includes data scraping, storing, DeepFM training and webpage visualization.

This project is an implementation of passage Building FPS Estimator System based on DeepFM - Long Yau.

The Estimator is based on <a href="https://github.com/ChenglongChen/tensorflow-DeepFM">DeepFM</a> (DeepFM: A Factorization-Machine based Neural Network for CTR Prediction - arXiv:1703.04247 [cs.IR]).


# Declaration
This project included data gathered from <a href="http://www.game-debate.com/">GAMEDEBATE</a>, <a href="http://www.userbenchmark.com/">UserBenchmark</a>, <a href="https://www.price.com.hk/">Price</a>, <a href="https://www.techpowerup.com/">techpowerup</a>.

All those data exclude userbench are gathered through data scraping using selenium webdriver.

# Installation
__Python__

This installation guide is based on Python 3.6.

DeepFM

- pip3 install numpy

- pip3 install scipy

- pip3 install pandas

- pip3 install matplotlin

- pip3 install sklearn

- pip3 install tensorflow


DeepFM Web Service

- pip3 install Flask

- pip3 install Flask-Cors


Selenium

- pip3 install selenium


AWS

- pip3 install boto3

# References
[1] Building FPS Estimator System based on DeepFM, Long Yau 

[2] DeepFM: A Factorization-Machine based Neural Network for CTR Prediction, Huifeng Guo, Ruiming Tang, Yunming Yey, Zhenguo Li, Xiuqiang He. (arXiv:1703.04247 [cs.IR])

# Acknowledgement
This project is built based on the following project:

[1] <a href="https://github.com/ChenglongChen/tensorflow-DeepFM">tensorflow-DeepFM</a>, ChenglongChen

[2] <a href="https://github.com/hexiangnan/neural_factorization_machine">neural_factorization_machine</a>, He Xiangnan

[3] <a href="https://www.seleniumhq.org/projects/webdriver/">Selenium WebDriver</a>, SeleniumHQ

[4] <a href="https://aws.amazon.com/tw/dynamodb/">Amazon DynamoDB</a>, AWS

[5] <a href="https://github.com/pallets/flask">Flask</a>, davidism

[6] <a href="https://github.com/spring-projects/spring-framework">Spring Framework</a>, sbrannen 
