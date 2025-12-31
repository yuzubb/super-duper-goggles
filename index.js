const axios = require('axios');

module.exports = async (req, res) => {
  // CORSの設定（必要に応じて）
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  // 環境変数からトークンを取得
  const PADLET_TOKEN = process.env.PADLET_TOKEN;

  try {
    const response = await axios.get('https://api.padlet.dev/v1/me', {
      headers: {
        'X-Padlet-Token': PADLET_TOKEN
      }
    });

    res.status(200).json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch Padlet data',
      details: error.message
    });
  }
};
