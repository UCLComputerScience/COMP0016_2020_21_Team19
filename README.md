# NHS4 Activity Diary

### The blog is ready to host content.

To add a blog post:

- Create a new file in [`docs/_posts`](docs/_posts) named according to the following format:

    `YEAR-MONTH-DAY-title.markdown`
    
    Where `YEAR` is a four-digit number, `MONTH` and `DAY` are both two-digit numbers

- The file must have a header enclosed in `---`
    ```
    ---
    layout: post
    title:  "Post Title"
    date:   2020-10-13 17:57:48 +0100
    categories: cat1, cat2
    author: Name
    ---
    ```
    note that the `layout` must always be `post`

- You can view a live preview of the blog post as you write it by running
    ```
    $ bundle exec jekyll serve --livereload
    ```
    within the [`docs`](docs/) directory

- Once the post is complete, it can be pushed to GitHub