from app.db.database import Base, engine

def reset_database():
    print("Apagando tabelas existentes...")
    Base.metadata.drop_all(bind=engine)
    print("Recriando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas recriadas com sucesso!")

if __name__ == "__main__":
    reset_database()