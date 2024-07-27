const express = require("express");
const { getData } = require("./SchemeController");
const router = express.Router();

router.post("/data", getData)

exports.router = router;