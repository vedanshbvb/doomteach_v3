const express = require('express');
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');
dotenv.config({ path: path.join(__dirname, '../../.env') });


const router = express.Router();

// Load OAuth2 credentials from environment variables
const CLIENT_ID = process.env.GOOGLE_CLIENT_ID;
const CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET;
const REDIRECT_URI = process.env.GOOGLE_REDIRECT_URI;

// // Log OAuth credentials to oauth_logs.txt
// const logPath = path.join(__dirname, '../../oauth_logs.txt');
// const logData = `CLIENT_ID: ${CLIENT_ID}\nCLIENT_SECRET: ${CLIENT_SECRET}\nREDIRECT_URI: ${REDIRECT_URI}\n\n`;

// fs.appendFile(logPath, logData, (err) => {
//   if (err) {
//     console.error('Failed to write to oauth_logs.txt:', err);
//   } qq
// });

// Scopes for uploading to YouTube
const SCOPES = ['https://www.googleapis.com/auth/youtube.upload'];

// Create an OAuth2 client
const oauth2Client = new google.auth.OAuth2(
  CLIENT_ID,
  CLIENT_SECRET,
  REDIRECT_URI
);

// Route 1: Redirect user to Google's OAuth2 consent screen
router.get('/auth/google', (req, res) => {
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
    prompt: 'consent',
  });
  res.redirect(authUrl);
});

// Route 2: Handle OAuth2 callback and exchange code for tokens
router.get('/auth/google/callback', async (req, res) => {
  const code = req.query.code;
  const redirect = req.query.redirect || '/oauth-success';
  if (!code) {
    return res.status(400).send('No code provided');
  }

  try {
    const { tokens } = await oauth2Client.getToken(code);
    req.session.tokens = tokens;
    // Redirect to the specified location (e.g., /#upload or /oauth-success)
    res.redirect(redirect);
  } catch (err) {
    console.error('Error exchanging code for tokens:', err);
    res.status(500).send('Authentication failed');
  }
});

// Route 3: Upload a local video to YouTube using stored tokens
router.post('/upload-video', async (req, res) => {
  if (!req.session.tokens) {
    return res.status(401).send('Not authenticated with Google');
  }

  oauth2Client.setCredentials(req.session.tokens);

  const youtube = google.youtube({ version: 'v3', auth: oauth2Client });
  const videoPath = path.join(__dirname, '../../media/final_video.mp4');

  if (!fs.existsSync(videoPath)) {
    return res.status(404).send('Video file not found');
  }

  try {
    const response = await youtube.videos.insert({
      part: ['snippet', 'status'],
      requestBody: {
        snippet: {
          title: 'Uploaded by DoomTeach',
          description: 'Video uploaded via DoomTeach app',
        },
        status: {
          privacyStatus: 'private',
        },
      },
      media: {
        body: fs.createReadStream(videoPath),
      },
    });

    res.json({ success: true, videoId: response.data.id });
  } catch (err) {
    console.error('Error uploading video:', err);
    res.status(500).send('Video upload failed');
  }
});

module.exports = router;
