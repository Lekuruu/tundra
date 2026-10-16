
# Modified sqlalchemy classes from solero/houdini:
# https://github.com/solero/houdini/tree/master/houdini/data/

from datetime import date, datetime, time, timedelta
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text
from sqlalchemy import (
    SmallInteger,
    ForeignKey,
    DateTime,
    Interval,
    Boolean,
    Integer,
    String,
    Date,
    Time,
    CHAR
)

import math

__all__ = [
    'Base',
    'Penguin',
    'Login',
    'Card',
    'CardStarterDeck',
    'PenguinCard',
    'Stamp',
    'StampGroup',
    'CoverStamp',
    'CoverItem',
    'PenguinStamp',
    'Item',
    'PenguinItem',
    'BuddyList',
    'BuddyRequest',
    'IgnoreList',
    'Character',
    'CharacterBuddy',
    'Postcard',
    'PenguinPostcard'
]

class Base(DeclarativeBase):
    pass

class Penguin(Base):
    __tablename__ = "penguin"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=text("nextval('\"penguin_id_seq\"'::regclass)"),
    )
    username: Mapped[str] = mapped_column(
        String(12), nullable=False, unique=True
    )
    nickname: Mapped[str] = mapped_column(
        String(30), nullable=False
    )
    password: Mapped[str] = mapped_column(
        CHAR(60), nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    registration_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    safe_chat: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    last_paycheck: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    minutes_played: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    moderator: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    stealth_moderator: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    character: Mapped[int | None] = mapped_column(
        ForeignKey("character.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    igloo: Mapped[int | None] = mapped_column(
        ForeignKey(
            "penguin_igloo_room.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )
    coins: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("500")
    )
    color: Mapped[int | None] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    head: Mapped[int | None] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    face: Mapped[int | None] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    neck: Mapped[int | None] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    body: Mapped[int | None] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    hand: Mapped[int | None] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    feet: Mapped[int | None] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    photo: Mapped[int | None] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    flag: Mapped[int | None] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    permaban: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    book_modified: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    book_color: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("1")
    )
    book_highlight: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("1")
    )
    book_pattern: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    book_icon: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("1")
    )
    agent_status: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    field_op_status: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    career_medals: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    agent_medals: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    last_field_op: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    com_message_read_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    ninja_rank: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    ninja_progress: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    fire_ninja_rank: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    fire_ninja_progress: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    water_ninja_rank: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    water_ninja_progress: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    snow_ninja_progress: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    snow_ninja_rank: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    ninja_matches_won: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    fire_matches_won: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    water_matches_won: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    snow_progress_fire_wins: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    snow_progress_water_wins: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    snow_progress_snow_wins: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    rainbow_adoptability: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    has_dug: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    puffle_handler: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    nuggets: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    walking: Mapped[int | None] = mapped_column(
        ForeignKey("penguin_puffle.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    opened_playercard: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    special_wave: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    special_dance: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    special_snowball: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    map_category: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    status_field: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    timer_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    timer_start: Mapped[time] = mapped_column(
        Time,
        nullable=False,
        server_default=text("'00:00:00'::time without time zone"),
    )
    timer_end: Mapped[time] = mapped_column(
        Time,
        nullable=False,
        server_default=text("'23:59:59'::time without time zone"),
    )
    timer_total: Mapped[timedelta] = mapped_column(
        Interval,
        nullable=False,
        server_default=text("'01:00:00'::interval"),
    )
    grounded: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    approval_en: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    approval_pt: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    approval_fr: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    approval_es: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    approval_de: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    approval_ru: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    rejection_en: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    rejection_pt: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    rejection_fr: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    rejection_es: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    rejection_de: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    rejection_ru: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )

    @property
    def penguin_age(self) -> int:
        return (datetime.now() - self.registration_date).days

    @property
    def badge_level(self) -> int:
        return min(5, math.ceil(self.penguin_age / 180))

    @property
    def account_type(self) -> str:
        return 'standard' if not self.is_member else 'member'

    @property
    def is_member(self) -> bool:
        return True # TODO

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.nickname

    @property
    def swid(self) -> str:
        return str(self.id)

class Login(Base):
    __tablename__ = 'login'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=text("nextval('\"login_id_seq\"'::regclass)"),
    )
    penguin_id: Mapped[int] = mapped_column(
        ForeignKey('penguin.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )
    date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    ip_hash: Mapped[str] = mapped_column(
        CHAR(255), nullable=False
    )
    minutes_played: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )

class Card(Base):
    __tablename__ = "card"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    set_id: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("1")
    )
    power_id: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    element: Mapped[str] = mapped_column(
        CHAR(1), nullable=False, server_default=text("'s'::bpchar")
    )
    color: Mapped[str] = mapped_column(
        CHAR(1), nullable=False, server_default=text("'b'::bpchar")
    )
    value: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("2")
    )
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default=text("''::character varying"),
    )

    def __repr__(self) -> str:
        return f'{self.id}|{self.element}|{self.value}|{self.color}|{self.power_id}'

class CardStarterDeck(Base):
    __tablename__ = 'card_starter_deck'

    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    card_id: Mapped[int] = mapped_column(
        ForeignKey("card.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("1")
    )

class PenguinCard(Base):
    __tablename__ = 'penguin_card'

    penguin_id: Mapped[int] = mapped_column(
        ForeignKey("penguin.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    card_id: Mapped[int] = mapped_column(
        ForeignKey("card.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("1")
    )
    member_quantity: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )

class Stamp(Base):
    __tablename__ = 'stamp'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("stamp_group.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    member: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    rank: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("1")
    )
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default=text("''::character varying"),
    )

    @property
    def rank_token(self) -> str:
        return {
            1: 'Easy',
            2: 'Medium',
            3: 'Hard',
            4: 'Extreme'
        }.get(self.rank, '')

class StampGroup(Base):
    __tablename__ = 'stamp_group'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("stamp_group.id", ondelete="CASCADE", onupdate="CASCADE")
    )

class CoverStamp(Base):
    __tablename__ = 'cover_stamp'

    penguin_id: Mapped[int] = mapped_column(
        ForeignKey("penguin.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    stamp_id: Mapped[int] = mapped_column(
        ForeignKey("stamp.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    x: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    y: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    rotation: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    depth: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )

class CoverItem(Base):
    __tablename__ = 'cover_item'

    penguin_id: Mapped[int] = mapped_column(
        ForeignKey("penguin.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    x: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    y: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    rotation: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    depth: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )

class PenguinStamp(Base):
    __tablename__ = 'penguin_stamp'

    penguin_id: Mapped[int] = mapped_column(
        ForeignKey("penguin.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    stamp_id: Mapped[int] = mapped_column(
        ForeignKey("stamp.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    recent: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )

class Item(Base):
    __tablename__ = 'item'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str | None] = mapped_column(
        String(50)
    )
    type: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("1")
    )
    cost: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    member: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    bait: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    patched: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    legacy_inventory: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    vanilla_inventory: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    epf: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    tour: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    release_date: Mapped[date] = mapped_column(
        Date, nullable=False, server_default=text("now()")
    )
    treasure: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    innocent: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )

    def is_color(self):
        return self.type == 1

    def is_head(self):
        return self.type == 2

    def is_face(self):
        return self.type == 3

    def is_neck(self):
        return self.type == 4

    def is_body(self):
        return self.type == 5

    def is_hand(self):
        return self.type == 6

    def is_feet(self):
        return self.type == 7

    def is_flag(self):
        return self.type == 8

    def is_photo(self):
        return self.type == 9

    def is_award(self):
        return self.type == 10

class PenguinItem(Base):
    __tablename__ = 'penguin_item'

    penguin_id: Mapped[int] = mapped_column(
        ForeignKey("penguin.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )

class BuddyList(Base):
    __tablename__ = 'buddy_list'

    penguin_id: Mapped[int] = mapped_column(
        ForeignKey('penguin.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
    )
    buddy_id: Mapped[int] = mapped_column(
        ForeignKey('penguin.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
        index=True,
    )
    best_buddy: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )

class BuddyRequest(Base):
    __tablename__ = 'buddy_request'

    penguin_id: Mapped[int] = mapped_column(
        ForeignKey('penguin.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
    )
    requester_id: Mapped[int] = mapped_column(
        ForeignKey('penguin.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
    )

class IgnoreList(Base):
    __tablename__ = 'ignore_list'

    penguin_id: Mapped[int] = mapped_column(
        ForeignKey('penguin.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
    )
    ignore_id: Mapped[int] = mapped_column(
        ForeignKey('penguin.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
        index=True,
    )

class Character(Base):
    __tablename__ = 'character'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(30), nullable=False
    )
    gift_id: Mapped[int | None] = mapped_column(
        ForeignKey('item.id', ondelete='CASCADE', onupdate='CASCADE')
    )
    stamp_id: Mapped[int | None] = mapped_column(
        ForeignKey('stamp.id', ondelete='CASCADE', onupdate='CASCADE')
    )

class CharacterBuddy(Base):
    __tablename__ = 'character_buddy'

    penguin_id: Mapped[int] = mapped_column(
        ForeignKey('penguin.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
    )
    character_id: Mapped[int] = mapped_column(
        ForeignKey('character.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
    )
    best_buddy: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )

class Postcard(Base):
    __tablename__ = 'postcard'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    cost: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("10")
    )
    enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )

class PenguinPostcard(Base):
    __tablename__ = 'penguin_postcard'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=text("nextval('\"penguin_postcard_id_seq\"'::regclass)"),
    )
    penguin_id: Mapped[int] = mapped_column(
        ForeignKey('penguin.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        index=True,
    )
    sender_id: Mapped[int | None] = mapped_column(
        ForeignKey('penguin.id', ondelete='CASCADE', onupdate='CASCADE'),
        index=True,
    )
    postcard_id: Mapped[int] = mapped_column(
        ForeignKey('postcard.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )
    send_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )
    details: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default=text("''::character varying")
    )
    has_read: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
