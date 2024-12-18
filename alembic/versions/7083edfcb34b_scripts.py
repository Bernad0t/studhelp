"""scripts

Revision ID: 7083edfcb34b
Revises: 374969549195
Create Date: 2024-12-17 23:57:36.671872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7083edfcb34b'
down_revision: Union[str, None] = '374969549195'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()

    # Функция для логирования изменений
    conn.execute(sa.text("""
    CREATE OR REPLACE FUNCTION log_changes()
    RETURNS TRIGGER AS $$
    BEGIN
        IF TG_OP = 'INSERT' THEN
            INSERT INTO main_log (operation_type, user_operator, changed_data)
            VALUES ('INSERT', SESSION_USER, ROW(NEW.*)::TEXT);
        ELSIF TG_OP = 'UPDATE' THEN
            INSERT INTO main_log (operation_type, user_operator, changed_data)
            VALUES ('UPDATE', SESSION_USER, ROW(OLD.*, NEW.*)::TEXT);
        ELSIF TG_OP = 'DELETE' THEN
            INSERT INTO main_log (operation_type, user_operator, changed_data)
            VALUES ('DELETE', SESSION_USER, ROW(OLD.*)::TEXT);
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """))

    # Создайте триггеры для каждой таблицы

    # Триггер для ReportOrm
    conn.execute(sa.text("""
    CREATE TRIGGER report_change
    AFTER INSERT OR UPDATE OR DELETE ON report
    FOR EACH ROW EXECUTE FUNCTION log_changes();
    """))

    # Триггер для CallOrm
    conn.execute(sa.text("""
    CREATE TRIGGER call_change
    AFTER INSERT OR UPDATE OR DELETE ON call
    FOR EACH ROW EXECUTE FUNCTION log_changes();
    """))

    # Триггер для StatusCallOrm
    conn.execute(sa.text("""
    CREATE TRIGGER status_call_change
    AFTER INSERT OR UPDATE OR DELETE ON statuscall
    FOR EACH ROW EXECUTE FUNCTION log_changes();
    """))

    # Триггер для CarsOrm
    conn.execute(sa.text("""
    CREATE TRIGGER cars_change
    AFTER INSERT OR UPDATE OR DELETE ON cars
    FOR EACH ROW EXECUTE FUNCTION log_changes();
    """))

    # Триггер для BrigadesOrm
    conn.execute(sa.text("""
    CREATE TRIGGER brigades_change
    AFTER INSERT OR UPDATE OR DELETE ON brigades
    FOR EACH ROW EXECUTE FUNCTION log_changes();
    """))

    # Триггер для CompositionsBrigadesOrm
    conn.execute(sa.text("""
    CREATE TRIGGER compositions_brigades_change
    AFTER INSERT OR UPDATE OR DELETE ON compositionsbrigades
    FOR EACH ROW EXECUTE FUNCTION log_changes();
    """))

    # Триггер для UsersOrm
    conn.execute(sa.text("""
    CREATE TRIGGER users_change
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION log_changes();
    """))

    # Триггер для main_log (обычно логи не логируются, но для примера мы оставим их здесь)
    conn.execute(sa.text("""
    CREATE TRIGGER main_log_change
    AFTER INSERT OR UPDATE OR DELETE ON main_log
    FOR EACH ROW EXECUTE FUNCTION log_changes();
    """))

    # Триггер для secret_data (обычно логи не логируются, но для примера мы оставим их здесь)
    conn.execute(sa.text("""
    CREATE TRIGGER secret_data_change
    AFTER INSERT OR UPDATE OR DELETE ON secret_data
    FOR EACH ROW EXECUTE FUNCTION log_changes();
    """))


def downgrade():
    conn = op.get_bind()

    # Удаление триггеров
    conn.execute(sa.text("DROP TRIGGER IF EXISTS report_change ON report;"))
    conn.execute(sa.text("DROP TRIGGER IF EXISTS call_change ON call;"))
    conn.execute(sa.text("DROP TRIGGER IF EXISTS status_call_change ON statuscall;"))
    conn.execute(sa.text("DROP TRIGGER IF EXISTS cars_change ON cars;"))
    conn.execute(sa.text("DROP TRIGGER IF EXISTS brigades_change ON brigades;"))
    conn.execute(sa.text("DROP TRIGGER IF EXISTS compositions_brigades_change ON compositionsbrigades;"))
    conn.execute(sa.text("DROP TRIGGER IF EXISTS users_change ON users;"))
    conn.execute(sa.text("DROP TRIGGER IF EXISTS main_log_change ON main_log;"))
    conn.execute(sa.text("DROP TRIGGER IF EXISTS secret_data_change ON secret_data;"))

    # Удаление функции
    conn.execute(sa.text("DROP FUNCTION IF EXISTS log_changes();"))
