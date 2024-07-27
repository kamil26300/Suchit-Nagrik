require("dotenv").config();
const mongoose = require("mongoose");

exports.getData = async (req, res) => {
  try {
    const { tags, state } = req.body;

    const data = await getDataFromRegex(tags, state);

    data
      ? res.status(200).json(data)
      : res.status(404).json({ error: "Error 404" });
  } catch (error) {
    console.error("Error finding data: ", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

const getDataFromRegex = async (tags, state) => {
  const collection = mongoose.connection.db.collection("schemes");

  const caseInsensitiveRegex = (item) => {
    return { $regex: item, $options: "i" };
  };
  const tagsInNameRegex = tags.map((tag) => ({
    "fields.schemeName": caseInsensitiveRegex(tag),
  }));
  const tagsInTagsRegex = tags.map((tag) => ({
    "fields.tags": caseInsensitiveRegex(tag),
  }));

  const stateRegex = caseInsensitiveRegex(state);

  const filters = [
    {
      $and: [
        ...tagsInNameRegex,
        state ? { "fields.schemeName": stateRegex } : {},
      ],
    },
    {
      $and: [
        ...tagsInNameRegex,
        state ? { "fields.beneficiaryState": stateRegex } : {},
      ],
    },
    {
      $and: [
        ...tagsInTagsRegex,
        state ? { "fields.beneficiaryState": stateRegex } : {},
      ],
    },
  ];

  for (let filter of filters) {
    const data = await collection
      .find(filter, {
        projection: {
          "fields.tags": 1,
          "fields.schemeName": 1,
          "fields.schemeCategory": 1,
          "fields.beneficiaryState": 1,
          "fields.briefDescription": 1,
          _id: 0,
        },
      })
      .toArray();
    if (data.length > 0) {
      return data;
    }
  }

  const pipelineForMostTags = [
    {
      $addFields: {
        matchedTags: {
          $filter: {
            input: tags,
            as: "tag",
            cond: {
              $anyElementTrue: {
                $map: {
                  input: "$fields.tags",
                  as: "fieldTag",
                  in: {
                    $regexMatch: {
                      input: "$$fieldTag",
                      regex: "$$tag",
                      options: "i", // case insensitive
                    },
                  },
                },
              },
            },
          },
        },
      },
    },
    {
      $addFields: {
        matchCount: { $size: "$matchedTags" },
      },
    },
    {
      $match: {
        matchCount: { $gt: 0 }, // Ensure at least one tag matches
        ...(state ? { "fields.beneficiaryState": stateRegex } : {}),
      },
    },
    {
      $sort: { matchCount: -1 }, // Sort by most matches first
    },
    {
      $group: {
        _id: "$matchCount",
        documents: { $push: "$$ROOT" },
      },
    },
    {
      $sort: { _id: -1 }, // Sort groups by matchCount descending
    },
    {
      $limit: 1, // Keep only the group with the highest matchCount
    },
    {
      $unwind: "$documents", // Unwind the documents array
    },
    {
      $replaceRoot: { newRoot: "$documents" }, // Replace the root with each document
    },
    {
      $project: {
        "fields.tags": 1,
        "fields.schemeName": 1,
        "fields.schemeCategory": 1,
        "fields.beneficiaryState": 1,
        "fields.briefDescription": 1,
        matchCount: 1,
        _id: 0,
      },
    },
  ];

  const data = await collection.aggregate(pipelineForMostTags).toArray();

  return data.length > 0 ? data : null;
};
