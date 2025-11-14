'use client';

import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import WeatherCalendar from '@/components/WeatherCalendar';

export default function Home() {
    const [query, setQuery] = useState('');
    const [chatMessages, setChatMessages] = useState([]);
    const [chatInput, setChatInput] = useState('');
    const [queryResults, setQueryResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [selectedImage, setSelectedImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const fileInputRef = useRef(null);
    const chatContainerRef = useRef(null);

    // 自动滚动到底部
    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [chatMessages]);

    // RAG Query功能 - 使用ChromaDB检索
    const handleQuery = async () => {
        if (!query.trim()) return;

        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`http://localhost:8000/api/search?q=${encodeURIComponent(query)}&top_k=5`);

            if (!response.ok) {
                throw new Error('Query failed');
            }

            const data = await response.json();
            setQueryResults(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    // Chat功能 - 与AI对话
    const handleChat = async () => {
        if (!chatInput.trim()) return;

        const userMessage = { role: 'user', content: chatInput };
        setChatMessages(prev => [...prev, userMessage]);
        setChatInput('');
        setLoading(true);

        try {
            const response = await fetch('http://localhost:8000/api/chat/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: chatInput,
                    history: chatMessages
                })
            });

            if (!response.ok) {
                throw new Error('Chat failed');
            }

            const data = await response.json();
            const aiMessage = { role: 'assistant', content: data.response };
            setChatMessages(prev => [...prev, aiMessage]);
        } catch (err) {
            const errorMessage = { role: 'assistant', content: `错误: ${err.message}` };
            setChatMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    // 处理图片选择
    const handleImageSelect = (e) => {
        const file = e.target.files?.[0];
        if (file) {
            setSelectedImage(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    // 处理图片分析
    const handleImageAnalysis = async () => {
        if (!selectedImage) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('image', selectedImage);
        if (chatInput.trim()) {
            formData.append('additional_info', chatInput);
        }

        try {
            const response = await fetch('http://localhost:8000/api/analyze-skin', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Image analysis failed');
            }

            const data = await response.json();

            // 添加用户消息
            const userMessage = {
                role: 'user',
                content: chatInput || '上传了皮肤照片进行分析',
                image: imagePreview
            };
            setChatMessages(prev => [...prev, userMessage]);

            // 构建AI回复
            let aiResponse = `**皮肤分析结果**\n\n${data.analysis}\n\n`;

            if (data.recommended_products && data.recommended_products.length > 0) {
                aiResponse += `**推荐产品**:\n`;
                data.recommended_products.forEach((product, idx) => {
                    aiResponse += `\n${idx + 1}. **${product.name}**`;
                    if (product.brand) aiResponse += ` - ${product.brand}`;
                    if (product.category) aiResponse += ` (${product.category})`;
                    aiResponse += `\n   相关度: ${product.relevance}`;
                    if (product.description) {
                        aiResponse += `\n   ${product.description.substring(0, 100)}...`;
                    }
                    aiResponse += '\n';
                });
            }

            const aiMessage = {
                role: 'assistant',
                content: aiResponse,
                products: data.recommended_products
            };
            setChatMessages(prev => [...prev, aiMessage]);

            // 自动保存皮肤分析记录
            autoSaveSkinCondition(
                chatInput || '上传了皮肤照片进行分析',
                data,
                imagePreview
            );

            // 清空输入
            setChatInput('');
            setSelectedImage(null);
            setImagePreview(null);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        } catch (err) {
            const errorMessage = { role: 'assistant', content: `分析错误: ${err.message}` };
            setChatMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    // 自动保存皮肤状况记录到localStorage
    const autoSaveSkinCondition = (condition, analysisResult = null, imageData = null) => {
        if (!condition || !condition.trim()) return;

        // 创建新记录
        const newRecord = {
            id: Date.now(),
            date: new Date().toISOString(),
            condition: condition,
            hasImage: !!imageData,
            imagePreview: imageData ? imageData.substring(0, 100) + '...' : null, // 保存图片预览标识
            analysis: analysisResult ? {
                skinType: analysisResult.skin_type,
                concerns: analysisResult.concerns,
                summary: analysisResult.analysis ? analysisResult.analysis.substring(0, 200) : null
            } : null
        };

        // 从localStorage获取现有记录
        const existingRecords = JSON.parse(localStorage.getItem('skinAnalysisHistory') || '[]');

        // 添加新记录到开头，保留最近20条
        const updatedRecords = [newRecord, ...existingRecords].slice(0, 20);

        // 保存到localStorage
        localStorage.setItem('skinAnalysisHistory', JSON.stringify(updatedRecords));

        console.log('自动保存皮肤记录:', newRecord);

        // 触发自定义事件，通知WeatherCalendar组件更新
        window.dispatchEvent(new Event('skinConditionUpdated'));
    };

    // 生成购买链接（搜索产品名称+品牌）
    const generateBuyLink = (productName, brand) => {
        const searchQuery = encodeURIComponent(`${brand} ${productName}`);
        return `https://www.amazon.com/s?k=${searchQuery}`;
    };

    return (
        <div className="min-h-screen bg-background">
            {/* Hero Section */}
            <section className="relative py-12 px-4 sm:px-6 lg:px-8">
                <div className="max-w-7xl mx-auto text-center">
                    <h1 className="text-4xl sm:text-5xl font-bold tracking-tight mb-4">
                        SkinMe
                    </h1>
                    <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-6">
                        基于EWG数据库 (7,933个产品)，使用RAG技术为您推荐安全有效的护肤品
                    </p>
                    <div className="flex flex-wrap justify-center gap-2">
                        <Badge variant="secondary">✅ ChromaDB向量检索</Badge>
                        <Badge variant="secondary">✅ OpenAI Embeddings</Badge>
                        <Badge variant="secondary">✅ RAG问答</Badge>
                        <Badge variant="secondary">✅ GPT-4 Vision 皮肤分析</Badge>
                    </div>
                </div>
            </section>

            {/* Main Content */}
            <section className="py-8 px-4 sm:px-6 lg:px-8">
                <div className="max-w-7xl mx-auto">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        {/* Left/Main Content - 2/3 width */}
                        <div className="lg:col-span-2">
                    <Tabs defaultValue="query" className="w-full">
                        <TabsList className="grid w-full grid-cols-2">
                            <TabsTrigger value="query">🔍 产品检索 (Query)</TabsTrigger>
                            <TabsTrigger value="chat">💬 AI对话 (Chat)</TabsTrigger>
                        </TabsList>

                        {/* Query Tab */}
                        <TabsContent value="query" className="space-y-4">
                            <Card className="p-6">
                                <h2 className="text-2xl font-semibold mb-4">智能产品检索</h2>
                                <p className="text-muted-foreground mb-4">
                                    使用语义搜索找到最相关的护肤品
                                </p>
                                <div className="space-y-4">
                                    <Input
                                        placeholder="例如: best moisturizer for dry sensitive skin"
                                        value={query}
                                        onChange={(e) => setQuery(e.target.value)}
                                        onKeyPress={(e) => e.key === 'Enter' && handleQuery()}
                                        className="text-lg"
                                    />
                                    <Button
                                        onClick={handleQuery}
                                        disabled={loading || !query.trim()}
                                        size="lg"
                                        className="w-full"
                                    >
                                        {loading ? '检索中...' : '🔍 检索产品'}
                                    </Button>
                                </div>

                                {error && (
                                    <div className="mt-4 p-4 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded">
                                        ❌ 错误: {error}
                                    </div>
                                )}
                            </Card>

                            {/* Query Results */}
                            {queryResults && queryResults.results && (
                                <div className="space-y-4">
                                    <h3 className="text-xl font-semibold">
                                        找到 {queryResults.results.length} 个相关产品
                                    </h3>
                                    {queryResults.results.map((item, idx) => (
                                        <Card key={idx} className="p-6 hover:shadow-lg transition-shadow">
                                            <div className="flex gap-4">
                                                {/* 产品图片 */}
                                                <div className="flex-shrink-0">
                                                    <img
                                                        src={item.image_url || `https://ui-avatars.com/api/?name=SK&size=200&background=6366f1&color=fff&bold=true`}
                                                        alt={item.product_name || `产品 ${idx + 1}`}
                                                        className="w-32 h-32 rounded-lg object-cover border-2 border-gray-200 dark:border-gray-700"
                                                        onError={(e) => {
                                                            e.target.src = `https://ui-avatars.com/api/?name=SK&size=200&background=6366f1&color=fff&bold=true`;
                                                        }}
                                                    />
                                                </div>

                                                {/* 产品信息 */}
                                                <div className="flex-1 space-y-3">
                                                    <div className="flex items-start justify-between">
                                                        <div className="flex-1">
                                                            <h4 className="text-xl font-bold text-blue-600 dark:text-blue-400">
                                                                {item.product_name || item.metadata?.book || `产品 ${idx + 1}`}
                                                            </h4>
                                                            {item.distance && (
                                                                <Badge variant="outline" className="mt-1">
                                                                    相似度: {(1 - item.distance).toFixed(3)}
                                                                </Badge>
                                                            )}
                                                        </div>
                                                    </div>

                                                    <div className="bg-muted p-4 rounded-lg">
                                                        <p className="text-sm whitespace-pre-wrap">
                                                            {item.document || item.text || '无描述'}
                                                        </p>
                                                    </div>

                                                    <div className="flex flex-wrap gap-2">
                                                        {/* 直接购买按钮（仅当有真实Amazon链接时显示） */}
                                                        {item.metadata?.amazon_url && (
                                                            <Button
                                                                size="sm"
                                                                className="bg-orange-500 hover:bg-orange-600"
                                                                onClick={() => {
                                                                    window.open(item.metadata.amazon_url, '_blank');
                                                                }}
                                                            >
                                                                🛒 Amazon直购
                                                            </Button>
                                                        )}

                                                        {/* Amazon搜索按钮（始终显示） */}
                                                        <Button
                                                            size="sm"
                                                            variant="outline"
                                                            onClick={() => {
                                                                const productName = item.product_name || item.metadata?.book || '';
                                                                window.open(generateBuyLink(productName, ''), '_blank');
                                                            }}
                                                        >
                                                            🔍 Amazon搜索
                                                        </Button>

                                                        {/* EWG评分按钮 */}
                                                        <Button
                                                            size="sm"
                                                            variant="outline"
                                                            onClick={() => {
                                                                const ewgUrl = item.metadata?.ewg_url;
                                                                if (ewgUrl) {
                                                                    window.open(ewgUrl, '_blank');
                                                                } else {
                                                                    const productName = item.product_name || item.metadata?.book || '';
                                                                    window.open(`https://www.ewg.org/skindeep/search/?search=${encodeURIComponent(productName)}`, '_blank');
                                                                }
                                                            }}
                                                        >
                                                            📊 EWG评分
                                                        </Button>
                                                    </div>
                                                </div>
                                            </div>
                                        </Card>
                                    ))}
                                </div>
                            )}
                        </TabsContent>

                        {/* Chat Tab */}
                        <TabsContent value="chat" className="space-y-4">
                            <Card className="p-6">
                                <h2 className="text-2xl font-semibold mb-4">AI护肤顾问 + 皮肤分析</h2>
                                <p className="text-muted-foreground mb-4">
                                    与AI对话获取护肤建议，或上传皮肤照片进行专业分析
                                </p>

                                {/* Chat Messages */}
                                <div
                                    ref={chatContainerRef}
                                    className="space-y-3 mb-4 h-[600px] overflow-y-auto scroll-smooth border rounded-lg p-4 bg-gray-50 dark:bg-gray-900"
                                >
                                    {chatMessages.length === 0 ? (
                                        <div className="text-center text-muted-foreground py-8">
                                            开始对话，询问关于护肤品的问题，或上传皮肤照片进行分析...
                                        </div>
                                    ) : (
                                        chatMessages.map((msg, idx) => (
                                            <div
                                                key={idx}
                                                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                                            >
                                                <div
                                                    className={`max-w-[80%] rounded-lg p-3 ${
                                                        msg.role === 'user'
                                                            ? 'bg-blue-500 text-white'
                                                            : 'bg-muted'
                                                    }`}
                                                >
                                                    {msg.image && (
                                                        <img
                                                            src={msg.image}
                                                            alt="用户上传"
                                                            className="max-w-xs rounded mb-2"
                                                        />
                                                    )}
                                                    <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                                                    {msg.products && msg.products.length > 0 && (
                                                        <div className="mt-3 space-y-2">
                                                            {msg.products.map((product, pidx) => (
                                                                <div key={pidx} className="bg-white dark:bg-gray-800 p-3 rounded text-gray-900 dark:text-gray-100">
                                                                    <p className="font-semibold">{product.name}</p>
                                                                    {product.brand && <p className="text-xs">{product.brand}</p>}
                                                                    <div className="flex gap-2 mt-2">
                                                                        {product.amazon_url && (
                                                                            <a
                                                                                href={product.amazon_url}
                                                                                target="_blank"
                                                                                rel="noopener noreferrer"
                                                                                className="text-xs bg-orange-500 text-white px-2 py-1 rounded hover:bg-orange-600"
                                                                            >
                                                                                🛒 购买
                                                                            </a>
                                                                        )}
                                                                        {product.ewg_url && (
                                                                            <a
                                                                                href={product.ewg_url}
                                                                                target="_blank"
                                                                                rel="noopener noreferrer"
                                                                                className="text-xs bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600"
                                                                            >
                                                                                📊 EWG
                                                                            </a>
                                                                        )}
                                                                    </div>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        ))
                                    )}
                                </div>

                                {/* Image Preview */}
                                {imagePreview && (
                                    <div className="mb-4">
                                        <div className="relative inline-block">
                                            <img
                                                src={imagePreview}
                                                alt="预览"
                                                className="max-w-xs rounded border-2 border-blue-500"
                                            />
                                            <button
                                                onClick={() => {
                                                    setImagePreview(null);
                                                    setSelectedImage(null);
                                                    if (fileInputRef.current) {
                                                        fileInputRef.current.value = '';
                                                    }
                                                }}
                                                className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600"
                                            >
                                                ✕
                                            </button>
                                        </div>
                                    </div>
                                )}

                                {/* Chat Input */}
                                <div className="space-y-2">
                                    <Textarea
                                        placeholder="例如: 我的皮肤很干燥，有什么好的保湿产品推荐？或描述您的皮肤状况..."
                                        value={chatInput}
                                        onChange={(e) => setChatInput(e.target.value)}
                                        onKeyPress={(e) => {
                                            if (e.key === 'Enter' && !e.shiftKey) {
                                                e.preventDefault();
                                                if (selectedImage) {
                                                    handleImageAnalysis();
                                                } else {
                                                    handleChat();
                                                }
                                            }
                                        }}
                                        rows={3}
                                    />

                                    <div className="flex gap-2">
                                        <input
                                            type="file"
                                            ref={fileInputRef}
                                            onChange={handleImageSelect}
                                            accept="image/*"
                                            className="hidden"
                                        />
                                        <Button
                                            onClick={() => fileInputRef.current?.click()}
                                            variant="outline"
                                            disabled={loading}
                                            className="flex-shrink-0"
                                        >
                                            📷 上传照片
                                        </Button>

                                        {selectedImage ? (
                                            <Button
                                                onClick={handleImageAnalysis}
                                                disabled={loading}
                                                className="flex-1 bg-green-600 hover:bg-green-700"
                                            >
                                                {loading ? '分析中...' : '🔍 分析皮肤'}
                                            </Button>
                                        ) : (
                                            <Button
                                                onClick={handleChat}
                                                disabled={loading || !chatInput.trim()}
                                                className="flex-1"
                                            >
                                                {loading ? '思考中...' : '💬 发送消息'}
                                            </Button>
                                        )}
                                    </div>
                                </div>
                            </Card>
                        </TabsContent>
                    </Tabs>
                        </div>

                        {/* Right Sidebar - Weather & Calendar - 1/3 width */}
                        <div className="lg:col-span-1">
                            <WeatherCalendar />
                        </div>
                    </div>
                </div>
            </section>

            {/* System Info */}
            <section className="py-8 px-4 sm:px-6 lg:px-8">
                <div className="max-w-6xl mx-auto">
                    <Card className="p-6">
                        <h3 className="text-xl font-semibold mb-3">系统状态</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                            <div>
                                <p className="text-muted-foreground">
                                    <strong>数据库:</strong> ChromaDB (7,933条产品数据)
                                </p>
                                <p className="text-muted-foreground">
                                    <strong>Embedding模型:</strong> OpenAI text-embedding-3-small (1536维)
                                </p>
                            </div>
                            <div>
                                <p className="text-muted-foreground">
                                    <strong>后端API:</strong>{' '}
                                    <a href="http://localhost:8000/docs" target="_blank" className="text-blue-500 hover:underline">
                                        http://localhost:8000/docs
                                    </a>
                                </p>
                                <p className="text-muted-foreground">
                                    <strong>ChromaDB:</strong> http://localhost:8001
                                </p>
                            </div>
                        </div>
                    </Card>
                </div>
            </section>
        </div>
    );
}
