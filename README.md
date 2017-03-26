# Application Purpose

The application, called periodically, will fetch an RSS feed URL and check
{title, author, description} for matches with a set of regular expressions.
Upon a match, it will send out notifications (email, and stdout are currently
supported).

# My Purpose

I made this to become more familiar with GitHub, and to brush off the rust
on my Python (four spaces, wut?). If someone finds this trivial piece of code
useful, great! Also, this is the third time I've written this script, and
since it was so trivial, I never thought to back it up outside of my OS
patition, disappearing every format. It'll be safe in the cloud. Right? Right?!
I'll, I intend to use it as a test bed for different storage engines, like
Amazon DynamoDB, etc. Hence the rediculous over-engineering of what might
otherwise have been a 20 line script.

# Technology

- _cron_ - this script is not a background service. It must be executed
         periodically by an external service, like cron.
- _SQLite_ - to maintain a list of previous matches in order to prevent
           duplicate emails, a database is maintained in SQLlite. SQLlite
           is under Public Domain.

# Required Libraries

- _html2text_ - Converts HTML content into Markdown. This is a short-term
			  solution until there's better encapsulation of a 'matched' RSS
			  item. https://github.com/aaronsw/html2text , licensed
			  under GLP 3.0