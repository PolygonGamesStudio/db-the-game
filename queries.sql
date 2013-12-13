use gamedb;

# вставка
INSERT INTO GameCharacter(Name,
        Level,
        Characteristics_Characteristics_id,
        Class_Class_id,
        User_User_id
        ) VALUES ("swirly62982860" ,
                "54" ,
                "966700" ,
                "7" ,
                "84739"
        );
# обновление
update GameCharacter set Name="Kratos" where GameCharacter_id=345;

# 13 (чёртова дюжина) персонажей, у которых больше всего побед
explain select GameCharacter_id,
            User_id,
            Login,
            Name,
            Level,
            Winner_id,
            Count_win
            from (
                select Winner_id,
                count(*) as Count_win
                from GameMatch
                group by Winner_id
                order by Count_win DESC
                limit 13
            ) as t
            join GameCharacter on t.winner_id = GameCharacter_id
            join User on User_User_id = User_id;

#количество игроков каждого класса
explain select Class_Class_id,
            Type,
            Count_class
            from (
                select Class_Class_id,
                count(*) as Count_class
                from GameCharacter
                group by Class_Class_id
                order by Count_class
                DESC limit 20
            ) as t
            join Class on Class_Class_id = Class_id;

#100 последних активных пользователей
explain select
                    User_id,
                    Login,
                    Registration_date,
                    Last_login_date,
                    Email,
                    is_active
                    from User
                    where is_active = 1
                    order by Last_login_date DESC
                    limit 100;

# все персонажи конкретного пользователя
explain select GameCharacter_id,
                    Name,
                    Level,
                    User_User_id,
                    Characteristics_Characteristics_id,
                    Class_Class_id
                    from GameCharacter
                    where User_User_id= 57 # вариативно
                    order by Level DESC;

# самый сильный предмет у персонажа
explain select Item_id,
                        Title,
                        max(Health + Armor + Damage + Manna)
                        from Characteristics
                        join Item on Characteristics_Characteristics_id = Characteristics_id
                        where GameCharacter_GameCharacter_id = 57; #

# инфа о матче по id, кто в нём учавствует и каких классов
select GameMatch_id,
            Title,
            Date_begin,
            Date_end,
            GameCharacter_id,
            Type,
            Name,
            Level
            from (
                select GameMatch_id,
                Title,
                Date_begin,
                Date_end
                from GameMatch where GameMatch_id = 57 # вариативно
            ) as t
            join Games on  GameMatch_GameMatch_id = GameMatch_id
            join GameCharacter on GameCharacter_GameCharacter_id = GameCharacter_id
            join Class on Class_Class_id = Class_id;

# среднее кол-во жизни, брони, урона, манны для каждого класса в игре
explain select Type,
                AVG(Health),
                AVG(Armor),
                AVG(Damage),
                AVG(Manna)
                from Ability
                join Class on Class_Class_id = Class_id
                join Characteristics on Characteristics_Characteristics_id = Characteristics_id
                group by Type;