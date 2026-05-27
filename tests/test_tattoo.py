"""Tests for agent_tattoo."""

import pytest
from datetime import datetime, timezone, timedelta

from agent_tattoo import (
    Tattoo,
    TattooCollection,
    TattooEarner,
    Condition,
    TattooStory,
    TattooDisplay,
    Visibility,
    TattooCategory,
)
from agent_tattoo.earner import milestone, achievement, failure


# ── Tattoo ────────────────────────────────────────────────────────


class TestTattoo:
    def test_create_basic(self):
        t = Tattoo(name="First Blood", description="Completed first mission")
        assert t.name == "First Blood"
        assert t.category == TattooCategory.EXPERIENCE
        assert t.visibility == Visibility.PUBLIC
        assert t.fade_level == 0.0
        assert t.id

    def test_empty_name_raises(self):
        with pytest.raises(ValueError):
            Tattoo(name="  ", description="x")

    def test_invalid_fade_raises(self):
        with pytest.raises(ValueError):
            Tattoo(name="t", description="x", fade_level=1.5)

    def test_age_days(self):
        past = datetime.now(timezone.utc) - timedelta(days=3)
        t = Tattoo(name="old", description="x", earned_at=past)
        assert t.age_days >= 3.0

    def test_fade(self):
        t = Tattoo(name="t", description="x", fade_level=0.5)
        t2 = t.fade(0.2)
        assert t2.fade_level == pytest.approx(0.7)
        assert t.fade_level == 0.5  # original unchanged
        assert t2.id == t.id  # same identity

    def test_fade_capped(self):
        t = Tattoo(name="t", description="x", fade_level=0.99)
        t2 = t.fade(0.5)
        assert t2.fade_level == 1.0

    def test_visibility_public(self):
        t = Tattoo(name="t", description="x")
        assert t.is_visible_to("public")
        assert t.is_visible_to("owner")
        assert t.is_visible_to("admin")
        assert t.is_visible_to("internal")

    def test_visibility_hidden(self):
        t = Tattoo(name="t", description="x", visibility=Visibility.HIDDEN)
        assert not t.is_visible_to("public")
        assert not t.is_visible_to("internal")
        assert t.is_visible_to("owner")

    def test_visibility_private(self):
        t = Tattoo(name="t", description="x", visibility=Visibility.PRIVATE)
        assert not t.is_visible_to("public")
        assert t.is_visible_to("admin")
        assert t.is_visible_to("owner")

    def test_to_dict_roundtrip(self):
        t = Tattoo(
            name="test",
            description="desc",
            category=TattooCategory.FAILURE,
            visibility=Visibility.INTERNAL,
        )
        d = t.to_dict()
        t2 = Tattoo.from_dict(d)
        assert t2.name == t.name
        assert t2.category == t.category
        assert t2.visibility == t.visibility
        assert t2.id == t.id

    def test_all_categories(self):
        for cat in TattooCategory:
            t = Tattoo(name="t", description="x", category=cat)
            assert t.category == cat

    def test_all_visibilities(self):
        for vis in Visibility:
            t = Tattoo(name="t", description="x", visibility=vis)
            assert t.visibility == vis


# ── TattooCollection ──────────────────────────────────────────────


class TestTattooCollection:
    def test_empty(self):
        c = TattooCollection()
        assert len(c) == 0
        assert list(c) == []

    def test_add_and_get(self):
        c = TattooCollection()
        t = Tattoo(name="t1", description="d1")
        c.add(t)
        assert len(c) == 1
        assert c.get(t.id) is t

    def test_add_duplicate_id_raises(self):
        c = TattooCollection()
        t = Tattoo(name="t1", description="d1")
        c.add(t)
        with pytest.raises(ValueError):
            c.add(t)

    def test_remove(self):
        c = TattooCollection()
        t = Tattoo(name="t1", description="d1")
        c.add(t)
        removed = c.remove(t.id)
        assert removed is t
        assert len(c) == 0

    def test_remove_nonexistent(self):
        c = TattooCollection()
        assert c.remove("nope") is None

    def test_contains(self):
        c = TattooCollection()
        t = Tattoo(name="t1", description="d1")
        c.add(t)
        assert t.id in c
        assert "nope" not in c

    def test_clear(self):
        c = TattooCollection()
        c.add(Tattoo(name="t1", description="d1"))
        c.add(Tattoo(name="t2", description="d2"))
        c.clear()
        assert len(c) == 0

    def test_by_category(self):
        c = TattooCollection()
        c.add(Tattoo(name="t1", description="d1", category=TattooCategory.MILESTONE))
        c.add(Tattoo(name="t2", description="d2", category=TattooCategory.FAILURE))
        c.add(Tattoo(name="t3", description="d3", category=TattooCategory.MILESTONE))
        assert len(c.by_category(TattooCategory.MILESTONE)) == 2
        assert len(c.by_category(TattooCategory.FAILURE)) == 1

    def test_by_visibility(self):
        c = TattooCollection()
        c.add(Tattoo(name="t1", description="d1", visibility=Visibility.HIDDEN))
        c.add(Tattoo(name="t2", description="d2", visibility=Visibility.PUBLIC))
        assert len(c.by_visibility(Visibility.PUBLIC)) == 1

    def test_visible_to(self):
        c = TattooCollection()
        c.add(Tattoo(name="t1", description="d1", visibility=Visibility.PUBLIC))
        c.add(Tattoo(name="t2", description="d2", visibility=Visibility.HIDDEN))
        assert len(c.visible_to("public")) == 1

    def test_search(self):
        c = TattooCollection()
        c.add(Tattoo(name="First Blood", description="won first battle"))
        c.add(Tattoo(name="Ghost", description="went undetected"))
        results = c.search("blood")
        assert len(results) == 1
        assert results[0].name == "First Blood"
        results = c.search("undetected")
        assert len(results) == 1

    def test_fresh_and_faded(self):
        c = TattooCollection()
        c.add(Tattoo(name="fresh", description="d", fade_level=0.1))
        c.add(Tattoo(name="mid", description="d", fade_level=0.5))
        c.add(Tattoo(name="old", description="d", fade_level=0.9))
        assert len(c.fresh(0.3)) == 1
        assert len(c.faded(0.7)) == 1

    def test_categories_stat(self):
        c = TattooCollection()
        c.add(Tattoo(name="t1", description="d", category=TattooCategory.MILESTONE))
        c.add(Tattoo(name="t2", description="d", category=TattooCategory.MILESTONE))
        c.add(Tattoo(name="t3", description="d", category=TattooCategory.FAILURE))
        cats = c.categories
        assert cats[TattooCategory.MILESTONE] == 2
        assert cats[TattooCategory.FAILURE] == 1

    def test_average_fade(self):
        c = TattooCollection()
        c.add(Tattoo(name="t1", description="d", fade_level=0.0))
        c.add(Tattoo(name="t2", description="d", fade_level=1.0))
        assert c.average_fade == pytest.approx(0.5)

    def test_average_fade_empty(self):
        assert TattooCollection().average_fade == 0.0

    def test_serialization_roundtrip(self):
        c = TattooCollection(owner="agent-007")
        c.add(Tattoo(name="t1", description="d1", category=TattooCategory.ACHIEVEMENT))
        c.add(Tattoo(name="t2", description="d2", visibility=Visibility.PRIVATE))
        d = c.to_dict()
        c2 = TattooCollection.from_dict(d)
        assert c2.owner == "agent-007"
        assert len(c2) == 2
        assert c2.get(c.all[0].id) is not None


# ── TattooEarner ──────────────────────────────────────────────────


class TestTattooEarner:
    def test_basic_condition(self):
        coll = TattooCollection()
        earner = TattooEarner(coll)
        cond = Condition(
            name="first-blood",
            description="First mission",
            tattoo_name="First Blood",
            tattoo_description="Completed first mission",
            check=lambda missions: missions >= 1,
        )
        earner.register(cond)
        earned = earner.check_all(missions=0)
        assert len(earned) == 0
        earned = earner.check_all(missions=1)
        assert len(earned) == 1
        assert earned[0].name == "First Blood"

    def test_one_shot(self):
        coll = TattooCollection()
        earner = TattooEarner(coll)
        cond = Condition(
            name="one-shot-test",
            description="test",
            tattoo_name="Test",
            tattoo_description="test",
            check=lambda: True,
            one_shot=True,
        )
        earner.register(cond)
        earned1 = earner.check_all()
        earned2 = earner.check_all()
        assert len(earned1) == 1
        assert len(earned2) == 0

    def test_repeatable(self):
        coll = TattooCollection()
        earner = TattooEarner(coll)
        cond = Condition(
            name="repeat",
            description="test",
            tattoo_name="Repeat",
            tattoo_description="test",
            check=lambda: True,
            one_shot=False,
        )
        earner.register(cond)
        earned1 = earner.check_all()
        earned2 = earner.check_all()
        assert len(earned1) == 1
        assert len(earned2) == 1

    def test_milestone_factory(self):
        coll = TattooCollection()
        earner = TattooEarner(coll)
        m = milestone("Veteran", "missions completed", lambda missions: missions, 100)
        earner.register(m)
        assert len(earner.check_all(missions=50)) == 0
        assert len(earner.check_all(missions=100)) == 1

    def test_achievement_factory(self):
        coll = TattooCollection()
        earner = TattooEarner(coll)
        a = achievement("Ghost", "undetected", lambda stealth: stealth is True)
        earner.register(a)
        assert len(earner.check_all(stealth=True)) == 1

    def test_failure_factory(self):
        coll = TattooCollection()
        earner = TattooEarner(coll)
        f = failure("Crash", "system crashed", lambda errors: errors > 0)
        earner.register(f)
        earned = earner.check_all(errors=5)
        assert len(earned) == 1
        assert earned[0].category == TattooCategory.FAILURE
        assert earned[0].visibility == Visibility.INTERNAL

    def test_pending(self):
        coll = TattooCollection()
        earner = TattooEarner(coll)
        c1 = Condition(name="a", description="", tattoo_name="A", tattoo_description="", check=lambda: False)
        c2 = Condition(name="b", description="", tattoo_name="B", tattoo_description="", check=lambda: True)
        earner.register(c1, c2)
        earner.check_all()
        pending = earner.pending()
        assert len(pending) == 1
        assert pending[0].name == "a"

    def test_evaluate_handles_bad_kwargs(self):
        cond = Condition(
            name="strict",
            description="",
            tattoo_name="S",
            tattoo_description="",
            check=lambda x: x > 0,
        )
        # passing wrong kwargs should return False, not raise
        assert cond.evaluate({}) is False


# ── TattooStory ───────────────────────────────────────────────────


class TestTattooStory:
    def test_add_entry(self):
        coll = TattooCollection()
        story = TattooStory(collection=coll)
        t = Tattoo(name="t1", description="d1")
        coll.add(t)
        entry = story.add_entry("Agent completed first mission", tattoos=[t])
        assert len(story.entries) == 1
        assert t.id in entry.tattoo_ids

    def test_timeline(self):
        coll = TattooCollection()
        story = TattooStory(collection=coll)
        t = Tattoo(name="t1", description="d1")
        coll.add(t)
        story.add_entry("Something happened", tattoos=[t], tags=["important"])
        tl = story.timeline()
        assert len(tl) == 1
        assert tl[0]["narrative"] == "Something happened"
        assert len(tl[0]["tattoos"]) == 1

    def test_search(self):
        story = TattooStory(collection=TattooCollection())
        story.add_entry("The agent infiltrated the base")
        story.add_entry("Retrieved the documents")
        results = story.search("infiltrated")
        assert len(results) == 1

    def test_by_tag(self):
        story = TattooStory(collection=TattooCollection())
        story.add_entry("Entry 1", tags=["combat"])
        story.add_entry("Entry 2", tags=["stealth"])
        assert len(story.by_tag("combat")) == 1

    def test_summary(self):
        coll = TattooCollection()
        story = TattooStory(collection=coll)
        t = Tattoo(name="t1", description="d1")
        coll.add(t)
        story.add_entry("Test", tattoos=[t])
        s = story.summary()
        assert "1 entries" in s
        assert "1 tattoos" in s

    def test_serialization_roundtrip(self):
        coll = TattooCollection()
        story = TattooStory(collection=coll)
        t = Tattoo(name="t1", description="d1")
        coll.add(t)
        story.add_entry("Test narrative", tattoos=[t], tags=["tag1"])
        d = story.to_dict()
        s2 = TattooStory.from_dict(d, coll)
        assert len(s2.entries) == 1
        assert s2.entries[0].narrative == "Test narrative"


# ── TattooDisplay ─────────────────────────────────────────────────


class TestTattooDisplay:
    def test_tattoo_to_text(self):
        t = Tattoo(name="First Blood", description="First mission done")
        text = TattooDisplay.tattoo_to_text(t)
        assert "First Blood" in text
        assert "First mission done" in text

    def test_collection_empty_text(self):
        c = TattooCollection()
        text = TattooDisplay.collection_as_text(c)
        assert "no tattoos" in text

    def test_collection_text(self):
        c = TattooCollection(owner="agent-x")
        c.add(Tattoo(name="T1", description="D1"))
        text = TattooDisplay.collection_as_text(c)
        assert "agent-x" in text
        assert "T1" in text

    def test_collection_markdown(self):
        c = TattooCollection(owner="agent-x")
        c.add(Tattoo(name="T1", description="D1", category=TattooCategory.ACHIEVEMENT))
        md = TattooDisplay.collection_as_markdown(c)
        assert "# " in md
        assert "T1" in md
        assert "Achievement" in md

    def test_collection_ascii(self):
        c = TattooCollection()
        c.add(Tattoo(name="T1", description="D1"))
        ascii_art = TattooDisplay.collection_as_ascii(c)
        assert "T1" in ascii_art
        assert "╱" in ascii_art

    def test_empty_ascii(self):
        c = TattooCollection()
        text = TattooDisplay.collection_as_ascii(c)
        assert "blank" in text.lower()

    def test_empty_markdown(self):
        c = TattooCollection()
        md = TattooDisplay.collection_as_markdown(c)
        assert "No tattoos" in md
