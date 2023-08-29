import sqlite3

CONN = sqlite3.connect('dogs.db')
CURSOR = CONN.cursor()


class Dog:
    all_dogs = []

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None

    def __repr__(self):
        return f'{self.id} {self.name} {self.breed}'

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS dogs (
        id INTEGER PRIMARY KEY,
        name TEXT, 
        breed TEXT) 
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
        DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
        INSERT INTO dogs (name, breed) VALUES(?,?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        new_dog_id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        self.id = new_dog_id
        return self


    @classmethod
    def create(cls, name, breed):
        new_dog = cls(name, breed)
        new_dog.save()
        new_dog_id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        dog_with_id = cls.find_by_id(new_dog_id)
        return dog_with_id

    @classmethod
    def new_from_db(cls, row):  # accept as a parameter the row that has been retrieved from the db
        dog = cls(row[1], row[2])  # set each row column as an attribute of the dog instance being created
        dog.id = row[0]  # set the 1st column from the db as the id of the object
        return dog

    @classmethod
    def get_all(cls):
        sql = """
        SELECT * FROM dogs
        """
        dogs_from_db = CURSOR.execute(sql)  # get all the dog records from the db
        cls.all_dogs = [cls.new_from_db(dog) for dog in dogs_from_db]  # update the all_dogs list with the new updated
        # dog instances that contain the dog ID numbers.
        return cls.all_dogs

    @classmethod
    def find_by_name(cls, name):
        # Dog.save()
        sql = """
        SELECT * FROM dogs
        WHERE name = ?
        LIMIT 1
        """
        found_dogs = CURSOR.execute(sql, (name,))
        for dog in found_dogs:
            return cls.new_from_db(dog)

    @classmethod
    def find_by_id(cls, dog_id):
        sql = """
        SELECT * FROM dogs
        WHERE id = ?
        """
        dog_found = CURSOR.execute(sql, (dog_id,))
        for dog in dog_found:
            return cls.new_from_db(dog)

    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
        SELECT * FROM dogs WHERE name = ? and breed = ?
        """
        dog_found = CURSOR.execute(sql,(name, breed))
        if dog_found is None:
            print("dog found")
            for dog in dog_found:
                return Dog.new_from_db(dog)
        else:
            print("no dog found")
            newly_created_dog = Dog.create(name, breed)
            return newly_created_dog

    def update(self):
        sql = """
        UPDATE dogs
        SET name = ? 
        WHERE id = ?
        """
        # dod_id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        CURSOR.execute(sql, (self.name, self.id))




doggy = Dog.create('samantha', 'zuri')
# dogs = CURSOR.execute("select * from dogs")
# for dog in dogs:
#     print(Dog.new_from_db(dog))

print(Dog.find_or_create_by('samanthaaa', 'zuri'))

