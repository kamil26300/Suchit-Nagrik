const express = require("express");
const { getData, getAnalytics } = require("./SchemeController");
const router = express.Router();

router.post("/data", getData).get("/analytics", getAnalytics)

exports.router = router;