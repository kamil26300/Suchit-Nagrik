const express = require("express");
const server = express();
const mongoose = require("mongoose");
const morgan = require("morgan");
const Scheme = require("./SchemeRoute");
require("dotenv").config();

server.use(express.json());
server.use(morgan("dev"));

server.use("/schemes", Scheme.router);

main().catch((err) => console.log(err));

async function main() {
  await mongoose.connect(
    process.env.MONGO_DB
  );
  console.log("DataBase connected");
}

server.get("/", (req, res) => {
  res.json({ status: "Success" });
});

server.listen(8080, () => {
  console.log("Server started");
});
