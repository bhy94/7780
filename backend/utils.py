import toml
from typing import List
from loguru import logger

def load_config():
    return toml.load("env.toml")

def parse_tag_names(tags: str) -> List[str]:
    return list(filter(lambda x:len(x) > 0, map( lambda x: x.strip(), tags.split(','))))

async def init_database_process(pool):
    logger.info("initializing database")
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:            

            await cur.execute("CREATE DATABASE shop")
            await cur.fetchall()

            await conn.commit()

    async with pool.acquire() as conn:
        async with conn.cursor() as cur: 

            await cur.execute("USE shop")
            await cur.fetchall()
            
            await cur.execute("""
                CREATE TABLE `login_status_admin` (
                `lsa_id` int NOT NULL AUTO_INCREMENT,
                `admin_id` int NOT NULL,
                `token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                `expire_time` datetime NOT NULL,
                PRIMARY KEY (`lsa_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            await cur.fetchall()

            await cur.execute("""
                CREATE TABLE `login_status_user` (
                `lsu_id` int NOT NULL AUTO_INCREMENT,
                `user_id` int NOT NULL,
                `token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                `expire_time` datetime NOT NULL,
                PRIMARY KEY (`lsu_id`),
                KEY `login_status_user_FK_user_id` (`user_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            await cur.fetchall()

            await cur.execute("""
                CREATE TABLE `login_status_vendor` (
                `lsv_id` int NOT NULL AUTO_INCREMENT,
                `vendor_id` int NOT NULL,
                `token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                `expire_time` datetime NOT NULL,
                PRIMARY KEY (`lsv_id`),
                KEY `login_status_vendor_FK_vendor_id` (`vendor_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            await cur.fetchall()

            await cur.execute("""
                CREATE TABLE `products` (
                `product_id` int NOT NULL AUTO_INCREMENT,
                `product_name` varchar(100) NOT NULL,
                `product_cover` varchar(500) DEFAULT NULL,
                `product_info` varchar(100) DEFAULT NULL,
                `product_score` decimal(10,0) DEFAULT NULL,
                `price` decimal(12,2) NOT NULL,
                PRIMARY KEY (`product_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

            """)
            await cur.fetchall()

            await cur.execute("""
                CREATE TABLE `tags` (
                `tag_id` int NOT NULL AUTO_INCREMENT,
                `tag_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                PRIMARY KEY (`tag_id`),
                UNIQUE KEY `tags_unique` (`tag_name`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            await cur.fetchall()

            await cur.execute("""
                CREATE TABLE `users` (
                `user_id` int NOT NULL AUTO_INCREMENT,
                `user_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                `user_password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                `user_display_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                `address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                `avatar` varchar(100) DEFAULT NULL,
                `telephone_number` varchar(100) DEFAULT NULL,
                `balance` decimal(12,2) NOT NULL,
                PRIMARY KEY (`user_id`),
                UNIQUE KEY `users_pk_username` (`user_username`),
                UNIQUE KEY `users_un_user_display_name` (`user_display_name`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            await cur.fetchall()

            await cur.execute("""
                CREATE TABLE `vendors` (
                `vendor_id` int NOT NULL AUTO_INCREMENT,
                `vendor_username` varchar(100) NOT NULL,
                `vendor_password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                `vendor_display_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                `origin_address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                `vendor_score` decimal(10,0) DEFAULT NULL,
                `avatar` varchar(100) DEFAULT NULL,
                `balance` decimal(12,2) DEFAULT NULL,
                PRIMARY KEY (`vendor_id`),
                UNIQUE KEY `vendors_un_vendor_username` (`vendor_username`),
                UNIQUE KEY `vendors_un_vendor_display_name` (`vendor_display_name`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            await cur.fetchall()

            await cur.execute("""
                CREATE TABLE `orders` (
                `order_id` int NOT NULL AUTO_INCREMENT,
                `user_id` int NOT NULL,
                `parent_order_id` int NOT NULL,
                `product_id` int NOT NULL,
                `quantity` int NOT NULL,
                `total_price` decimal(10,0) DEFAULT NULL,
                `place_time` datetime NOT NULL,
                `status` varchar(100) NOT NULL,
                `express_number` varchar(100) DEFAULT NULL,
                PRIMARY KEY (`order_id`),
                KEY `orders_FK_users` (`user_id`),
                KEY `orders_FK_products` (`product_id`),
                KEY `orders_FK_parent_order` (`parent_order_id`),
                CONSTRAINT `orders_FK_products` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
                CONSTRAINT `orders_FK_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            await cur.fetchall()

            await cur.execute("""
                CREATE TABLE `tag_product_rel` (
                `tp_rel_id` int NOT NULL AUTO_INCREMENT,
                `tag_id` int NOT NULL,
                `product_id` int NOT NULL,
                PRIMARY KEY (`tp_rel_id`),
                KEY `tag_product_rel_FK_tag_id` (`tag_id`),
                KEY `tag_product_rel_FK_product_id` (`product_id`),
                CONSTRAINT `tag_product_rel_FK_product_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
                CONSTRAINT `tag_product_rel_FK_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            await cur.fetchall()

            await cur.execute("""
                CREATE TABLE `vendor_product_rel` (
                `vp_rel_id` int NOT NULL AUTO_INCREMENT,
                `vendor_id` int NOT NULL,
                `product_id` int NOT NULL,
                PRIMARY KEY (`vp_rel_id`),
                KEY `vendor_product_rel_FK_vendor_id` (`vendor_id`),
                KEY `vendor_product_rel_FK_product_id` (`product_id`),
                CONSTRAINT `vendor_product_rel_FK_product_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
                CONSTRAINT `vendor_product_rel_FK_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`vendor_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            await cur.fetchall()
            
            await conn.commit()

    async with pool.acquire() as conn:
        async with conn.cursor() as cur: 
            await cur.execute("USE shop")
            await cur.fetchall()

            await cur.executemany("""
                INSERT INTO users(user_username, user_password, user_display_name, address, avatar, telephone_number, balance) VALUES(%s, %s, %s, %s, %s, %s, %s)
            """, [
                ("bob", "bob123", "Bob", "88 Queensway, Admiralty, Hong Kong", "/imgs/a1.jpg", "+852 6123 4567", 10000),
                ("alice", "alice123", "Alice", "27 Science Park Road, Shatin, Hong Kong", "/imgs/a2.jpg", "+852 6789 1234", 5000),
                ("john", "john123", "John", "6 Lakeside Road, West Kowloon, Hong Kong", "/imgs/a3.jpg", "+852 5555 8888", 12.5)
            ])

            await cur.executemany("""
                INSERT INTO vendors(vendor_username, vendor_password, vendor_display_name, origin_address, vendor_score, avatar, balance) VALUES(%s, %s, %s, %s, 5, %s, %s)
            """, [
                ("test", "test123", "Quality Mobile Phone Sales", "HKBU, Kowloon Tong, Hong Kong", "/imgs/a12.jpg", 0),
            ])

            await cur.executemany("""
                INSERT INTO products(product_name, product_cover, product_info, product_score, price) VALUES(%s, %s, %s, 5, %s)
            """, [
                ("Huawei P40 Pro", "/imgs/p1.jpg", "Capturing the crown as best camera phone of 2020, Huawei P40 Pro making every shot a masterpiece", 5999),
                ("Huawei Mate 60", "/imgs/p2.jpg", "The Huawei Mate 60, acclaimed as the best camera phone of 2021, ensuring vivid and detailed images", 8999),
                ("Xiaomi Mi 10", "/imgs/p3.jpg", "The Xiaomi Mi 10 stands out as the best budget phone of 2020, offering powerful performance.", 299),
                ("Xiaomi Redmi 9", "/imgs/p4.jpg", "As the best budget phone of 2020, the Xiaomi Redmi Note 9 delivers exceptional value.", 999),
                ("Xiaomi 14", "/imgs/p5.jpg", "The Xiaomi 14 continues the legacy as the best budget phone of 2020.", 3999)
            ])

            await cur.executemany("""
                INSERT INTO tags(tag_name) VALUES (%s)
            """, [
                ('Expensive',),
                ('Cheap',),
                ('New',),
                ('Old',),
            ])

            await cur.executemany("""
                INSERT INTO tag_product_rel(tag_id, product_id) VALUES (%s, %s)
            """, [
                (1, 1),
                (1, 2),
                (1, 5),
                (2, 3),
                (2, 4),
                (3, 2),
                (3, 5),
                (4, 1),
                (4, 3),
                (4, 4),
            ])

            await cur.executemany("""
                INSERT INTO vendor_product_rel(vendor_id, product_id) VALUES (%s, %s)
            """ , [
                (1, 1),
                (1, 2),
                (1, 3),
                (1, 4),
                (1, 5)
            ])


            await cur.executemany("""
                INSERT INTO orders(user_id, parent_order_id, product_id, quantity, total_price, place_time, status, express_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """ , [
                (2, 1, 2, 1, 8999, "2024-03-20 12:00:00", "shipping", "SF123456"),
                (2, 2, 1, 1, 5999, "2024-03-26 18:00:00", "paid", ""),
            ])

            await conn.commit()