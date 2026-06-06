import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db.database import Base
from backend.models.conversation import Conversation
from backend.models.custom_agent import CustomAgent as CustomAgentModel
from backend.models.user import User
from backend.utils import manage_agent


def _make_test_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine, testing_session_local


def test_manage_agent_create_agent(monkeypatch):
    engine, testing_session_local = _make_test_session()
    monkeypatch.setattr(manage_agent, "SessionLocal", testing_session_local)
    monkeypatch.setattr(manage_agent, "_register_runtime_agent", lambda db_agent: None)

    db = testing_session_local()
    user = User(username="tester", email="tester@example.com", password_hash="hash")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    payload = {
        "current_user_id": user.id,
        "name": "data_agent",
        "description": "handles summaries",
        "system_prompt": "You summarize data tasks.",
        "llm_adapter": "tongyi",
        "tools": ["web_search", "rag_retrieval"],
        "icon": "analytics",
    }

    result = json.loads(manage_agent.create_agent(json.dumps(payload)))
    assert result["status"] == "success"
    assert result["action"] == "create"
    assert result["name"] == "data_agent"

    db = testing_session_local()
    saved = db.query(CustomAgentModel).filter(CustomAgentModel.agent_id == result["agent_id"]).first()
    assert saved is not None
    assert saved.user_id == user.id
    assert saved.tools == ["web_search", "rag_retrieval"]
    assert saved.icon == "analytics"
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_manage_agent_update_agent_with_conversation_context(monkeypatch):
    engine, testing_session_local = _make_test_session()
    monkeypatch.setattr(manage_agent, "SessionLocal", testing_session_local)
    monkeypatch.setattr(manage_agent, "_register_runtime_agent", lambda db_agent: None)

    db = testing_session_local()
    user = User(username="owner", email="owner@example.com", password_hash="hash")
    db.add(user)
    db.commit()
    db.refresh(user)

    conversation = Conversation(user_id=user.id, title="Agent Admin")
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    agent = CustomAgentModel(name="support_agent", agent_id="custom_support_001", user_id=user.id, icon="support", description="old description", system_prompt="old prompt", llm_adapter="tongyi", tools=[])
    db.add(agent)
    db.commit()
    db.close()

    payload = {
        "conversation_id": conversation.id,
        "target_name": "support_agent",
        "name": "after_sales_agent",
        "description": "handles after-sales requests",
        "system_prompt": "You handle after-sales support.",
        "llm_adapter": "deepseek",
        "tools": ["web_search"],
    }

    result = json.loads(manage_agent.update_agent(json.dumps(payload)))
    assert result["status"] == "success"
    assert result["action"] == "update"
    assert result["name"] == "after_sales_agent"
    assert result["llm_adapter"] == "deepseek"

    db = testing_session_local()
    updated = db.query(CustomAgentModel).filter(CustomAgentModel.agent_id == "custom_support_001").first()
    assert updated.name == "after_sales_agent"
    assert updated.description == "handles after-sales requests"
    assert updated.system_prompt == "You handle after-sales support."
    assert updated.tools == ["web_search"]
    db.close()
    Base.metadata.drop_all(bind=engine)
