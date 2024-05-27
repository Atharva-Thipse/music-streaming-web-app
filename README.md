# Music-Streaming-Web-App

wsl terminal 1: redis-server (to run redis server)
This command starts the Redis server in the first WSL terminal. Redis is an open-source, in-memory data structure store used as a database, cache, and message broker. It's commonly used in web development for tasks like caching and managing queues.

wsl terminal 2: ~/go/bin/MailHog (to run MailHog server)
This command starts MailHog server in the second WSL terminal. MailHog is a tool used for SMTP testing. It captures and displays emails sent by your application during development, allowing you to inspect them without sending them to real email addresses.

wsl terminal 3: cd backend --> celery -A tasks.celery worker --loglevel=info
This command starts a Celery worker in the third WSL terminal. Celery is a distributed task queue that is used to process background jobs asynchronously in web applications. The -A tasks.celery option specifies the Celery app instance to use, and --loglevel=info sets the log level to info.

wsl terminal 4: cd backend --> celery -A tasks.celery beat --loglevel=info
This command starts the Celery beat scheduler in the fourth WSL terminal. Celery beat is a scheduler that sends tasks to the Celery worker at specified intervals. It's commonly used for periodic tasks like sending emails or generating reports. The --loglevel=info option sets the log level to info.

powershell terminal 1: cd music-streaming-app --> npm run serve (to run Vue.js server)

powershell terminal 2: (to run app.py)

make sure to install node_modules by running "npm install".
