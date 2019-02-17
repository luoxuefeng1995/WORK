```mysql
CREATE DATABASE total_detail;


CREATE TABLE total_cs(
    ID int(11) unsigned AUTO_INCREMENT,
    totalcs varchar(50) NOT NULL,
    vegecsname varchar(50) NOT NULL,
    vegename varchar(50) NOT NULL,
    PRIMARY KEY (ID),
    UNIQUE KEY (vegename)
);  最后结尾不能用‘逗号’
```



```mysql
CREATE TABLE detaildata(
	ID int(11) unsigned AUTO_INCREMENT,
    vege_name varchar(50) NOT NULL,
    type varchar(50) NOT NULL,
    id_number varchar(50) NOT NULL,
    name varchar(50),
    cook_df varchar(30),
    cook_time varchar(30),
    rate varchar(10),
    PRIMARY KEY (ID),
    FOREIGN KEY (vege_name) REFERENCES total_cs(vegename)
)
```

```mysql
INSERT INTO total_cs ('totalcs', 'vegecsname', 'vegename') VALUES()
```

```mysql
INSERT INTO detaildata ('vege_name', 'type', 'id_number', 'name', 'cook_df', 'cook_time', 'rate') VALUES()
```

