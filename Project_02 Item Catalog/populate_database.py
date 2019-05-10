from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Base, Movie, User


engine = create_engine('sqlite:///Movie_Genre.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(name="John Doe", email="johndoe@gmail.com",
             picture='https://nicolealvares.files.'
                     'wordpress.com/2013/10/making-of-the'
                     '-worlds-first-camera-thumb.jpg')
             
session.add(User1)
session.commit()

# Movie comedy
movies = Genre(user_id=1, name="Comedy")

session.add(movies)
session.commit()

Item2 = Movie(user_id=1, name="Smallfoot",
              description="Mythical Creatures, Unlikely Friendships",
              price="$9.99", ratings="PG", genre=movies)

session.add(Item2)
session.commit()


Item1 = Movie(user_id=1, name="Teen Titans Go! To the Movies",
              description="Big Break, Heroic Mission, Unlikely Heroes",
              price="$9.99", ratings="PG", genre=movies)

session.add(Item1)
session.commit()

Item2 = Movie(user_id=1, name="The House with a Clock in Its Walls",
              description="Curses and Spells, Wizards and Magicians",
              price="$5.50", ratings="PG", genre=movies)

session.add(Item2)
session.commit()

Item3 = Movie(user_id=1, name="Ferdinand",
              description="Coming Home, Non-Traditional Families",
              price="$3.99", ratings="PG", genre=movies)

session.add(Item3)
session.commit()

Item4 = Movie(user_id=1, name="Spaceballs",
              description="Space Wars, Robots and Androids, Unlikely Heroes",
              price="$3.99", ratings="PG", genre=movies)

session.add(Item4)
session.commit()

Item5 = Movie(user_id=1, name="Space Jam",
              description="Basketball Players, Evil Aliens, Heroic Mission",
              price="$12.99", ratings="PG", genre=movies)

session.add(Item5)
session.commit()

Item6 = Movie(user_id=1, name="Shrek the Third",
              description="Fantasy Lands, Talking Animals, Crowned Heads, "
                          "Curses and Spells, Fish Out of Water, "
                          "Mythical Creatures",
              price="$.99", ratings="NR", genre=movies)

session.add(Item6)
session.commit()

Item7 = Movie(user_id=1, name="Dr. Seuss' The Grinch",
              description="Conspiracies, Crime Sprees, Metamorphosis, "
                          "Unlikely Friendships, Unlikely Heroes",
              price="$13.49", ratings="PG", genre=movies)

session.add(Item7)
session.commit()


# Action movies
movies2 = Genre(user_id=1, name="Action")

session.add(movies2)
session.commit()


Item1 = Movie(user_id=1, name="Incredibles 2",
              description="Heroic Mission, Unlikely Heroes",
              price="$19.99", ratings="PG", genre=movies2)

session.add(Item1)
session.commit()

Item2 = Movie(user_id=1, name="Christopher Robin",
              description="Starting Over, Toys Come to Life, "
                          "Unlikely Friendships",
              price="$25", ratings="PG", genre=movies2)

session.add(Item2)
session.commit()

Item3 = Movie(user_id=1, name="Moana",
              description="Chosen One, Curses and Spells, "
                          "Heroic Mission, Lost Worlds, "
                          "Priceless Artifacts and Prized Objects",
              price="$15", ratings="PG", genre=movies2)

session.add(Item3)
session.commit()

Item4 = Movie(user_id=1, name="Sherlock Gnomes",
              description="Amateur Sleuths, Kidnapping, Star Detectives, "
                          "Toys Come to Life",
              price="$12", ratings="PG", genre=movies2)

session.add(Item4)
session.commit()

Item5 = Movie(user_id=1, name="Johnny English Strikes Again",
              description="Betrayal, Computer Paranoia, "
                          "Hijackings, Virtual Reality.",
              price="$14", ratings="PG", genre=movies2)

session.add(Item5)
session.commit()

Item6 = Movie(user_id=1, name="The Jungle Book ",
              description="	Monkeys, Survival in the Wilderness, "
                          "Talking Animals.",
              price="$12", ratings="PG", genre=movies2)

session.add(Item6)
session.commit()


# Thriller movies
movies = Genre(user_id=1, name="Thriller")

session.add(movies)
session.commit()


Item1 = Movie(user_id=1, name="Ocean's 8", description="Jewel Theft.",
                     price="$8.99", ratings="PG13", genre=movies)

session.add(Item1)
session.commit()

Item2 = Movie(user_id=1, name="The Darkest Minds",
              description="Escape From Prison, Future Dystopias, "
                          "On the Run, Redemption.",
              price="$6.99", ratings="PG13", genre=movies)

session.add(Item2)
session.commit()

Item3 = Movie(user_id=1, name="The Post",
              description="	Conspiracies, Fighting the System, "
                          "Office Politics, Scandals and Cover-Up",
              price="$9.95", ratings="PG13", genre=movies)

session.add(Item3)
session.commit()

Item4 = Movie(user_id=1, name="Non-Stop",
              description="	Air Disasters, Hijackings, "
                          "Race Against Time, Trapped or Confined.",
              price="$6.99", ratings="PG13", genre=movies)

session.add(Item4)
session.commit()


# Horror Movies
movies = Genre(user_id=1, name="Horror")

session.add(movies)
session.commit()


Item1 = Movie(user_id=1, name="Halloween",
              description="Crime Sprees, Escape From Prison, "
                          "Haunted By the Pas.",
              price="$2.99", ratings="R", genre=movies)

session.add(Item1)
session.commit()

Item2 = Movie(user_id=1, name="The Nun",
              description="Demonic Possession, "
                          "Members of the Clergy, Suicide",
              price="$5.99", ratings="R", genre=movies)

session.add(Item2)
session.commit()

Item3 = Movie(user_id=1, name="Hotel Artemis",
              description="Future Dystopias, Secret Organizations",
              price="$4.50", ratings="R", genre=movies)

session.add(Item3)
session.commit()

Item4 = Movie(user_id=1, name="Bad Times at the El Royale",
              description="Crime Sprees, Keeping a Secret",
              price="$6.95", ratings="R", genre=movies)

session.add(Item4)
session.commit()

Item5 = Movie(user_id=1, name="Red Sparrow",
              description="Femmes Fatales, Switching Sides, "
                          "Traitorous Spies",
              price="$7.95", ratings="R", genre=movies)

session.add(Item5)
session.commit()


# War movie
movies = Genre(user_id=1, name="War")

session.add(movies)
session.commit()


Item1 = Movie(user_id=1, name="Fury",
              description="	Heroic Mission, Military Life",
              price="$13.95", ratings="R", genre=movies)

session.add(Item1)
session.commit()

Item2 = Movie(user_id=1, name="	Zero Dark Thirty",
              description="Assassination Plots, Heroic Mission, Terrorism",
              price="$4.95", ratings="R", genre=movies)

session.add(Item2)
session.commit()

Item3 = Movie(user_id=1, name="Hacksaw Ridge",
              description="Great Battles, Message From God, Military Life",
              price="$6.95", ratings="R", genre=movies)

session.add(Item3)
session.commit()

Item4 = Movie(user_id=1, name="	Dunkirk",
              description="Great Battles, Heroic Mission, "
                          "War At Sea, War in the Sky",
              price="$13.95", ratings="PG13", genre=movies)

session.add(Item4)
session.commit()

Item5 = Movie(user_id=1, name="Behind Enemy Lines",
              description="Behind Enemy Lines, Daring Rescues, "
                          "Heroic Mission",
              price="$7.95", ratings="PG13", genre=movies)

session.add(Item5)
session.commit()


# SciFi movie
movies = Genre(user_id=1, name="SciFi")

session.add(movies)
session.commit()


Item1 = Movie(user_id=1, name="The Predator",
              description="Evil Aliens",
              price="$9.95", ratings="R", genre=movies)

session.add(Item1)
session.commit()

Item2 = Movie(user_id=1, name="Ready Player One",
              description="Chicken cooked in Marsala "
                          "wine sauce with mushrooms",
              price="$7.95", ratings="PG", genre=movies)

session.add(Item2)
session.commit()

Item3 = Movie(user_id=1, name="Potstickers",
              description="Bounty Hunters, Computer Paranoia, "
                          "Future Dystopias, Priceless.",
              price="$6.50", ratings="PG13", genre=movies)

session.add(Item3)
session.commit()

Item4 = Movie(user_id=1, name="Sorry to Bother You",
              description="Assumed Identities, Big Break, "
                          "Double Life, Schemes and Ruses",
              price="$16.75", ratings="PG13", genre=movies)

session.add(Item4)
session.commit()


# Documentary
movies = Genre(user_id=1, name="Documentary")

session.add(movies)
session.commit()

Item9 = Movie(user_id=1, name="WHAT'S THE MATTER WITH KANSAS",
              description="Down on Their Luck, Religious "
                          "Zealotry, Underdogs",
              price="$8.99", ratings="NR", genre=movies)

session.add(Item9)
session.commit()


Item1 = Movie(user_id=1, name="Woodstock",
              description="Generation Gap, Bohemian Life",
              price="$2.99", ratings="R", genre=movies)

session.add(Item1)
session.commit()

Item2 = Movie(user_id=1, name="Undefeated",
              description="Documentary",
              price="$10.95", ratings="PG13", genre=movies)

session.add(Item2)
session.commit()

Item3 = Movie(user_id=1, name="Get Thrashed: The Story of Thrash Metal",
              description="Explore the blistering rise, brutal fall, and "
                          "lasting impact of thrash metal",
              price="$7.50", ratings="PG13", genre=movies)

session.add(Item3)
session.commit()

Item4 = Movie(user_id=1, name="Where Was God?",
              description="This inspirational documentary follows the "
                          "aftermath of the May 20, 2013 tornado "
                          "that devastated Moore, Oklahoma",
              price="$8.95", ratings="PG", genre=movies)

session.add(Item4)
session.commit()


session.add(Item2)
session.commit()

Item10 = Movie(user_id=1, name="MANNY",
               description="In Training, Boxers",
               price="$1.99", ratings="PG13", genre=movies)

session.add(Item10)
session.commit()


# Anime Movie
movies = Genre(user_id=1, name="Anime")

session.add(movies)
session.commit()


Item1 = Movie(user_id=1, name="Spirited Away ",
              description="Journey of Self-Discovery, Mythical Creatures, "
                          "Fantasy Lands",
              price="$5.95", ratings="PG", genre=movies)

session.add(Item1)
session.commit()

Item2 = Movie(user_id=1, name="Princess Mononoke",
              description="Heroic Mission, Mythical "
                          "Creatures, Righting the Wronged.",
              price="$17.99", ratings="PG", genre=movies)

session.add(Item2)
session.commit()


movies = Genre(user_id=1, name="Fantasy")
session.add(movies)
session.commit()

Item1 = Movie(user_id=1, name="Dog Days",
              description="Expecting a Baby, Intersecting Lives, "
                          "Looking For Love, Man's Best Friend",
              price="$5.95", ratings="PG", genre=movies)

session.add(Item1)
session.commit

Item1 = Movie(user_id=1, name="The Shape of Water",
              description="Living With Disability, "
                          "Mutants, On the Run, Workplace Romance",
              price="$16.95", ratings="R", genre=movies)

session.add(Item1)
session.commit()


Item1 = Movie(user_id=1, name="	Isle of Dogs",
              description="Conspiracies, Daring Rescues, "
                          "Future Dystopias, Talking Animals",
              price="$14.25", ratings="R", genre=movies)

session.add(Item1)
session.commit()


print("added menu items!")
