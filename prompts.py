OLOG_EXAMPLE = """{
  "claim": "The moon does not exist",
  "olog": {
    "nodes": [
      {
        "id": "1",
        "text": "The moon exists",
        "type": "fact",
        "source": "Astronomical observations and scientific consensus"
      },
      {
        "id": "2",
        "text": "Conspiracy theories",
        "type": "motivation",
        "details": "Some individuals may promote the idea that the moon does not exist as part of a larger conspiracy theory."
      },
      {
        "id": "3",
        "text": "Misinterpretation of evidence",
        "type": "error",
        "details": "Some may misinterpret or disregard scientific evidence due to lack of knowledge or confirmation bias."
      },
      {
        "id": "4",
        "text": "Moon landing hoaxes",
        "type": "related-claim",
        "details": "Related to false claims that the moon landings were faked and therefore promote the idea that the moon might not be real."
      },
      {
        "id": "5",
        "text": "Satellite imagery",
        "type": "evidence",
        "details": "Photos and data from satellites and space missions provide evidence of the moon's existence."
      }
    ],
    "edges": [
      {
        "source": "2",
        "target": "1",
        "relation": "contradicts"
      },
      {
        "source": "3",
        "target": "1",
        "relation": "misunderstands"
      },
      {
        "source": "4",
        "target": "1",
        "relation": "misrepresents"
      },
      {
        "source": "5",
        "target": "1",
        "relation": "supports"
      }
    ]
  }
}"""