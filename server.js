const express = require('express')
const cors = require('cors')
const sql = require('sqlite3').verbose()

const app = express()
const PORT = 3000

app.use(express.json())

const db = new sql.Database('jobs.db', (err) => {
  if (err) {
    console.error('Could not connect to database', err);
  } else {
    console.log('Connected to SQLite database');
  }
});

app.get('/',(req,res)=>{
  const query = 'SELECT * FROM jobs'
  db.all(query,(err,result)=>{
    if(err){
      res.status(500).json({
        error : "Error at db"
      })
      return
    }
    res.status(200).json(result)
  })
})




app.listen(PORT,()=>{
  console.log(`Server started at ${PORT}`)
})