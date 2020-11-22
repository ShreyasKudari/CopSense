const express = require('express')
const app = express()
const http = require('http')

const server = http.createServer(app)
const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://pranshul:iamnotsimp@cluster0.2etod.mongodb.net/codechella?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true });


app.get("/", async (req, res) => {
    client.connect(async (err) => {
        const collection = client.db("codechella").collection("data")
        var dataSet = []
        var cursor = collection.find()
        const ok = cursor.forEach((element => {
            return new Promise(async (resolve, reject) => {
                dataSet.push(element)
                resolve()
            })
        })
        )
        let kk = await ok
        res.send(dataSet)
    })
})


server.listen(5000)