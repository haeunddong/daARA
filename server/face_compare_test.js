const AWS = require('aws-sdk')
AWS.config.update({region:'ap-northeast-2'});
const bucket        = 'daara2021.03.15test' // the bucketname without s3://
const photo_source  = '예상 화면.png'
const photo_target  = '전준휘 증명사진.jpg'
const photo = '전준휘 증명사진.jpg'
const config = new AWS.Config({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION
})
const client = new AWS.Rekognition();
const params = {
  
  SourceImage: {
    S3Object: {
      Bucket: bucket,
      Name: photo_source
    },
  },
  TargetImage: {
    S3Object: {
      Bucket: bucket,
      Name: photo_target
    },
  },
  SimilarityThreshold: 70
}


client.compareFaces(params, function(err, response) {
  if (err) {
    console.log(err, err.stack); // an error occurred
  } else {
    response.FaceMatches.forEach(data => {
      let position   = data.Face.BoundingBox
      let similarity = data.Similarity
      console.log(`The face at: ${position.Left}, ${position.Top} matches with ${similarity} % confidence`)
    }) // for response.faceDetails
  } // if
});

const params_2 = {
  Image: {
    S3Object: {
      Bucket: bucket,
      Name: photo
    },
  },
  Attributes: ['ALL']
}

client.detectFaces(params_2, function(err, response) {
  if (err) {
    console.log(err, err.stack); // an error occurred
  } else {
    console.log(`Detected faces for: ${photo}`)
    response.FaceDetails.forEach(data => {
      let low  = data.AgeRange.Low
      let high = data.AgeRange.High
      console.log(`The detected face is between: ${low} and ${high} years old`)
      console.log("All other attributes:")
      console.log(`  Age.Range.Low:          ${data.AgeRange.Low}`)
      console.log(`  Age.Range.High:         ${data.AgeRange.High}`)
      console.log(`  Smile.Value:            ${data.Smile.Value}`)
      console.log(`  Smile.Confidence:       ${data.Smile.Confidence}`)
      console.log(`  Emotions[0].Type:       ${data.Emotions[0].Type}`)
      console.log(`  Emotions[0].Confidence: ${data.Emotions[0].Confidence}`)
      console.log("------------")
      console.log("")
    }) // for response.faceDetails
  } // if
});

