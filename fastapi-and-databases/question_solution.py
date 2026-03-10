from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, update, delete

engine = create_engine("mysql+pymysql://root:@localhost/student_db")

metadata = MetaData()

students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("age", Integer),
    Column("city", String(50), nullable=True)
)

metadata.create_all(engine)

conn = engine.connect()

insert_query = students.insert().values([
    {"name": "Rahul", "age": 22, "city": "Delhi"},
    {"name": "Amit", "age": 19, "city": "Mumbai"},
    {"name": "Priya", "age": 21, "city": "Pune"}
])

conn.execute(insert_query)

print("All Students:")
select_query = select(students)
result = conn.execute(select_query)

for row in result:
    print(row)

update_query = (
    update(students)
    .where(students.c.name == "Rahul")
    .values(city="Bangalore")
)

conn.execute(update_query)

delete_query = delete(students).where(students.c.age < 20)

conn.execute(delete_query)

print("\nAfter Update and Delete:")

result = conn.execute(select(students))

for row in result:
    print(row)

conn.close()

poar = students.insert().values(name="Sita", age=20, city="Chennai")