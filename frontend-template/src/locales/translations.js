export const translations = {
  zh: {
    // Header
    appName: 'SkinMe - AI 护肤助手',

    // Main Page - Tabs
    queryTab: '🔍 产品检索',
    chatTab: '💬 AI对话',
    photoTab: '📷 拍照分析',
    historyTab: '📋 历史记录',

    // Chat Section
    chatTitle: '与 AI 护肤助手对话',
    chatPlaceholder: '描述你的皮肤问题或需求...',
    sendButton: '发送',
    uploading: '上传中...',
    analyzing: '分析中...',

    // Photo Analysis Section
    photoTitle: '上传皮肤照片进行 AI 分析',
    uploadButton: '选择照片',
    analyzeButton: '开始分析',
    photoPlaceholder: '请先上传一张清晰的皮肤照片',
    descriptionPlaceholder: '可选：描述你的皮肤问题或关注点...',

    // Analysis Results
    analysisResults: '分析结果',
    skinType: '肤质类型',
    skinConcerns: '皮肤问题',
    detailedAnalysis: '详细分析',
    recommendations: '产品推荐',
    noRecommendations: '暂无推荐产品',

    // Weather Calendar Sidebar
    todayDate: '今日日期',
    todayWeather: '当前天气',
    currentLocation: '当前位置',
    feelsLike: '体感',
    temperature: '温度',
    humidity: '湿度',
    uvIndex: '紫外线指数',
    skinAdvice: '护肤建议',
    skinConditionHistory: '皮肤状况记录',
    noRecords: '还没有记录',
    recentRecords: '最近记录',
    addRecord: '添加记录',
    recordPlaceholder: '记录今天的皮肤状况... (例如：今天皮肤有点干燥)',
    saveRecord: '💾 保存记录',
    cancelRecord: '取消',
    loading: '加载中...',
    loadingWeather: '正在获取天气信息...',
    locationError: '无法获取位置，使用默认位置',
    locationNotSupported: '浏览器不支持地理定位',
    weather: '天气',
    skinType: '肤质',
    concerns: '问题',

    // Weather advice
    weatherHot: '🌡️ 高温天气，注意防晒和补水',
    weatherCold: '❄️ 气温较低，加强保湿防护',
    weatherDry: '💧 空气干燥，使用保湿精华',
    weatherHumid: '💦 湿度较高，使用清爽型产品',
    weatherSunny: '☀️ 晴朗天气，务必涂抹防晒',
    weatherNormal: '天气适宜，正常护肤即可',

    // Tags
    photoTag: '📷 照片',
    aiAnalysisTag: '🤖 AI分析',

    // Product Card
    viewDetails: '查看详情',
    ingredients: '成分',
    safetyScore: '安全评分',

    // Query Section
    queryTitle: '智能产品检索',
    queryDescription: '使用语义搜索找到最相关的护肤品',
    queryPlaceholder: '例如: best moisturizer for dry sensitive skin',
    queryButton: '🔍 检索产品',
    querying: '检索中...',
    resultsFound: '找到',
    resultsProducts: '个相关产品',
    similarity: '相似度',
    noDescription: '无描述',
    buyOnAmazon: '🛒 Amazon直购',
    searchAmazon: '🔍 Amazon搜索',
    ewgRating: '📊 EWG评分',

    // Chat with Analysis
    chatAnalysisTitle: 'AI护肤顾问 + 皮肤分析',
    chatAnalysisDescription: '与AI对话获取护肤建议，或上传皮肤照片进行专业分析',
    chatStartMessage: '开始对话，询问关于护肤品的问题，或上传皮肤照片进行分析...',
    chatPlaceholderLong: '例如: 我的皮肤很干燥，有什么好的保湿产品推荐？或描述您的皮肤状况...',
    uploadPhoto: '📷 上传照片',
    analyzeSkin: '🔍 分析皮肤',
    sendMessage: '💬 发送消息',
    analyzing2: '分析中...',
    thinking: '思考中...',
    userUploaded: '用户上传',
    buyButton: '🛒 购买',

    // Hero Section
    heroDescription: '基于EWG数据库 (7,933个产品)，使用RAG技术为您推荐安全有效的护肤品',
    badge1: '✅ ChromaDB向量检索',
    badge2: '✅ OpenAI Embeddings',
    badge3: '✅ RAG问答',
    badge4: '✅ GPT-4 Vision 皮肤分析',

    // System Info
    systemStatus: '系统状态',
    database: '数据库',
    databaseInfo: 'ChromaDB (7,933条产品数据)',
    embeddingModel: 'Embedding模型',
    embeddingInfo: 'OpenAI text-embedding-3-small (1536维)',
    backendAPI: '后端API',

    // Error Messages
    errorAnalysis: '分析错误',
    errorMessage: '错误',

    // Common
    loading: '加载中...',
    error: '出错了',
    retry: '重试',
    close: '关闭',
  },

  en: {
    // Header
    appName: 'SkinMe - AI Skincare Assistant',

    // Main Page - Tabs
    queryTab: '🔍 Product Search',
    chatTab: '💬 AI Chat',
    photoTab: '📷 Photo Analysis',
    historyTab: '📋 History',

    // Chat Section
    chatTitle: 'Chat with AI Skincare Assistant',
    chatPlaceholder: 'Describe your skin concerns or needs...',
    sendButton: 'Send',
    uploading: 'Uploading...',
    analyzing: 'Analyzing...',

    // Photo Analysis Section
    photoTitle: 'Upload Skin Photo for AI Analysis',
    uploadButton: 'Choose Photo',
    analyzeButton: 'Start Analysis',
    photoPlaceholder: 'Please upload a clear photo of your skin first',
    descriptionPlaceholder: 'Optional: Describe your skin concerns...',

    // Analysis Results
    analysisResults: 'Analysis Results',
    skinType: 'Skin Type',
    skinConcerns: 'Skin Concerns',
    detailedAnalysis: 'Detailed Analysis',
    recommendations: 'Product Recommendations',
    noRecommendations: 'No recommendations available',

    // Weather Calendar Sidebar
    todayDate: "Today's Date",
    todayWeather: "Current Weather",
    currentLocation: 'Current Location',
    feelsLike: 'Feels like',
    temperature: 'Temperature',
    humidity: 'Humidity',
    uvIndex: 'UV Index',
    skinAdvice: 'Skincare Advice',
    skinConditionHistory: 'Skin Condition Records',
    noRecords: 'No records yet',
    recentRecords: 'Recent Records',
    addRecord: 'Add Record',
    recordPlaceholder: 'Record your skin condition today... (e.g., My skin feels a bit dry today)',
    saveRecord: '💾 Save Record',
    cancelRecord: 'Cancel',
    loading: 'Loading...',
    loadingWeather: 'Loading weather information...',
    locationError: 'Unable to get location, using default',
    locationNotSupported: 'Geolocation not supported by browser',
    weather: 'Weather',
    skinType: 'Skin Type',
    concerns: 'Concerns',

    // Weather advice
    weatherHot: '🌡️ Hot weather, remember sunscreen and hydration',
    weatherCold: '❄️ Cold weather, boost moisturizing protection',
    weatherDry: '💧 Dry air, use moisturizing serum',
    weatherHumid: '💦 High humidity, use lightweight products',
    weatherSunny: '☀️ Sunny weather, apply sunscreen',
    weatherNormal: 'Weather is suitable, normal skincare routine',

    // Tags
    photoTag: '📷 Photo',
    aiAnalysisTag: '🤖 AI Analysis',

    // Product Card
    viewDetails: 'View Details',
    ingredients: 'Ingredients',
    safetyScore: 'Safety Score',

    // Query Section
    queryTitle: 'Smart Product Search',
    queryDescription: 'Use semantic search to find the most relevant skincare products',
    queryPlaceholder: 'e.g., best moisturizer for dry sensitive skin',
    queryButton: '🔍 Search Products',
    querying: 'Searching...',
    resultsFound: 'Found',
    resultsProducts: 'relevant products',
    similarity: 'Similarity',
    noDescription: 'No description',
    buyOnAmazon: '🛒 Buy on Amazon',
    searchAmazon: '🔍 Search Amazon',
    ewgRating: '📊 EWG Rating',

    // Chat with Analysis
    chatAnalysisTitle: 'AI Skincare Advisor + Skin Analysis',
    chatAnalysisDescription: 'Chat with AI for skincare advice, or upload skin photos for professional analysis',
    chatStartMessage: 'Start chatting, ask about skincare products, or upload a skin photo for analysis...',
    chatPlaceholderLong: 'e.g., My skin is very dry, what moisturizer do you recommend? Or describe your skin condition...',
    uploadPhoto: '📷 Upload Photo',
    analyzeSkin: '🔍 Analyze Skin',
    sendMessage: '💬 Send Message',
    analyzing2: 'Analyzing...',
    thinking: 'Thinking...',
    userUploaded: 'User uploaded',
    buyButton: '🛒 Buy',

    // Hero Section
    heroDescription: 'Based on EWG database (7,933 products), using RAG technology to recommend safe and effective skincare products',
    badge1: '✅ ChromaDB Vector Search',
    badge2: '✅ OpenAI Embeddings',
    badge3: '✅ RAG Q&A',
    badge4: '✅ GPT-4 Vision Skin Analysis',

    // System Info
    systemStatus: 'System Status',
    database: 'Database',
    databaseInfo: 'ChromaDB (7,933 product records)',
    embeddingModel: 'Embedding Model',
    embeddingInfo: 'OpenAI text-embedding-3-small (1536 dims)',
    backendAPI: 'Backend API',

    // Error Messages
    errorAnalysis: 'Analysis error',
    errorMessage: 'Error',

    // Common
    loading: 'Loading...',
    error: 'An error occurred',
    retry: 'Retry',
    close: 'Close',
  }
};

// Hook to use translations
export const useTranslations = (language) => {
  return translations[language] || translations.zh;
};
