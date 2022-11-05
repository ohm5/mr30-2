MR30
===

Attempt to read MR30 (this one of semester 2/2565) and put in database and provide interface to query it.

## Database seeding
- Server reads from an sqlite3 file. The file should be generate by python script `parse_pdf.py`. The script will work with python 3.8

```
# install requirements first. (likely to be broken)
pip -r requirements.txt

# run
./parse_pdf.py <path to the MR30 pdf file>
```

- The sqlite3 database should be generated if nothing goes wrong. run python dev server with
```
python ./server.py
```

- `fe` folder contains a basic Vue.js front end. Run the development server by
```
cd fe
npm run dev
```

## Deploying

Pack the front end with
```bash
npm run build
```

optimized files will be put in `fe/dist`. The server serves this as static file.

Deploy to fly.io with
```
flyctl deploy
```
