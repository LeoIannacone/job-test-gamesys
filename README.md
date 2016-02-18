Job Test Gamesys
================

Hi!

This is my solution to the job test!

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

You can run tests via:
```
python manage.py tests
```

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

You can also check **lint** and run **tests** with:
```
./node_modules/.bin/gulp lint
./node_modules/.bin/gulp test
```

## The Friends List Problem

The Facebook Graph API v2 **does not allow to get the full Friends list of a User**, but it returns only the ones that have granted permission to the same App. In other word, a App can see only the its own users.
 - *Solution*: use `taggable_friends` instead of `friends` call in Graph per user:
   - **Pro**: you can get the whole list of the users
   - **Cons**:
     - it does not return the Facebook ID of the user, so you can't make associations in DB between users and friends
     - webhooks cannot work
