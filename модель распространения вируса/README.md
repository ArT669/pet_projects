# Модель распространения вируса.

Использованные библиотеки:


![](https://img.shields.io/badge/random-grey?style=flat-square) ![](https://img.shields.io/badge/matplotlib-blue?style=flat-square&logo=matplotlib) ![](https://img.shields.io/badge/numpy-grey?style=flat-square&logo=numpy&logoColor=white)
=======
![](https://img.shields.io/badge/random-grey?style=flat-square) ![](https://img.shields.io/badge/matplotlib-blue?style=flat-square&logo=matplotlib) ![](https://img.shields.io/badge/numpy-green?style=flat-square&logo=numpy)
>>>>>>> Stashed changes

Вдохновлялся [этим симулятором](https://tachyondecay.github.io/epidemic-simulator/). При желании можете прочитать [статью](https://nplus1.ru/material/2019/12/26/epidemic-math).

Написан клеточный автомат с модификацией для распространения вируса: создается некоторое количество агентов, которые могут ходить по миру, заражать других и болеть в разных стадиях, умирать.

Входной файл (data.txt) описывает основные характеристики всех групп агентов(людей).

В самой програме задаётся размер мира (количество клеток N*N), начальное количество агентов любой группы и их расположение, количество дней существования мира.

Есть несколько групп людей.

![](https://img.shields.io/badge/0-008000?style=plastic) - здоровый;

![](https://img.shields.io/badge/1-ff0000?style=plastic) - инфицированный;

![](https://img.shields.io/badge/2-ff1493?style=plastic) - легко больной;

![](https://img.shields.io/badge/3-000000?style=plastic) - тяжело больной;

![](https://img.shields.io/badge/4-0000ff?style=plastic) - имунный;

![](https://img.shields.io/badge/5-blue?style=plastic) - мертвый.

Для каждой группы существуют характеристики: шаг движения по миру, вероятность заразить другого, радиус заражения, время инкубационного периода и вероятность перехода из одной группы в другую. 

Например, если ![](https://img.shields.io/badge/1-ff0000?style=plastic) может перейти в ![](https://img.shields.io/badge/3-000000?style=plastic) с вероятностью 0.7 - это значит, что болезнь чаще всего проходит в тяжелой форме.

На выходе получаем визуализацию клеточного автомата в виде "до" и "после" с подробным описанием сколько агентов в каждой из групп и общей картиной мира.

![Figure_1](https://github.com/ArT669/pet_projects/assets/120614279/640f29d9-c589-4268-a14e-2a41a50d004b)

![Figure_2](https://github.com/ArT669/pet_projects/assets/120614279/eae84353-ae7e-4ba1-a219-de42388e4146)


Процесс заражения в виде гифки



