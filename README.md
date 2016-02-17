Job Test Gamesys
================

Hi!

This is my solution the the job test!

## Run server
You have to install deps for the server
```
pip install -r requirements-vendor.txt -t lib
pip install -r requirements-local.txt -t lib
```

And then:
```
dev_appserver.py app.yaml
```

A running instance can be found here: [https://job-test-gamesys.appspot.com/friends](https://job-test-gamesys.appspot.com/friends)

### Build the client
You have to build the client if you want to run it locally. It's written in React.JS and packed with Webpack:

```
cd friends/app
npm install
```

**Build** with:
```
./node_modules/.bin/gulp build
```

You can run also a **eslint** check and the **tests** with:
```
./node_modules/.bin/gulp lint
./node_modules/.bin/gulp test
```

## Problems
I found some problems during implementation:

 1. The Facebook Graph API v2 **does not allow to get the full Friends list of a User**, but it returns only the ones that have granted permission to the same App. In other word, a App can see only the its own users.
  - *Solution*: use `taggable_friends` instead of `friends` call in Graph per user:
    - **Pro**: you can get the whole list of the users
    - **Cons**:
      - it does not return the Facebook ID of the user, so you can't make associations in DB between users and friends
      - webhooks cannot work

 2. **Webhooks are not working (or I did something wrong on Facebook side)**. However I have written complete tests for the verification (via GET requests) and to check signature in the POST requests as described in [webhooks doc](https://developers.facebook.com/docs/graph-api/webhooks/v2.5). You can see them [here](blob/master/webhooks/tests/tests.py).

   It looks like, after some tests adding and removing friends (which have granted permission to the App) no webhooks is correctly received. However the verification was fine:
  ![subscription.png](http://i.imgur.com/PrdwTqh.png)

  I have added a view at link `/webhooks-debug` which shows the webhooks the Application receives, but so far it shows only some tests I did.
