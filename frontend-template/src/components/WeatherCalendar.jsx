'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

export default function WeatherCalendar() {
    const [weather, setWeather] = useState(null);
    const [currentDate, setCurrentDate] = useState(new Date());
    const [skinCondition, setSkinCondition] = useState('');
    const [savedConditions, setSavedConditions] = useState([]);
    const [location, setLocation] = useState(null);
    const [locationError, setLocationError] = useState(null);
    const [isClient, setIsClient] = useState(false);

    // 标记客户端已加载
    useEffect(() => {
        setIsClient(true);
    }, []);

    // 获取天气信息
    useEffect(() => {
        if (isClient) {
            getUserLocation();
        }
    }, [isClient]);

    // 更新日期
    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDate(new Date());
        }, 60000); // 每分钟更新一次
        return () => clearInterval(timer);
    }, []);

    // 从localStorage加载皮肤状况记录
    useEffect(() => {
        const saved = localStorage.getItem('skinConditions');
        if (saved) {
            setSavedConditions(JSON.parse(saved));
        }
    }, []);

    // 获取用户地理位置
    const getUserLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    setLocation({ latitude, longitude });
                    fetchWeatherByLocation(latitude, longitude);
                    setLocationError(null);
                },
                (error) => {
                    console.error('Error getting location:', error);
                    setLocationError('无法获取位置，使用默认位置');
                    // 如果无法获取位置，使用默认位置或IP定位
                    fetchWeatherByIP();
                }
            );
        } else {
            setLocationError('浏览器不支持地理定位');
            fetchWeatherByIP();
        }
    };

    // 根据经纬度获取天气
    const fetchWeatherByLocation = async (lat, lon) => {
        try {
            // 使用 wttr.in API，支持经纬度查询
            const response = await fetch(`https://wttr.in/${lat},${lon}?format=j1`);
            const data = await response.json();
            setWeather(data);
        } catch (error) {
            console.error('Failed to fetch weather by location:', error);
            fetchWeatherByIP();
        }
    };

    // 根据IP获取天气（备用方案）
    const fetchWeatherByIP = async () => {
        try {
            // wttr.in 会自动根据IP定位
            const response = await fetch('https://wttr.in/?format=j1');
            const data = await response.json();
            setWeather(data);
        } catch (error) {
            console.error('Failed to fetch weather:', error);
            // 设置默认天气
            setWeather({
                current_condition: [{
                    temp_C: '--',
                    weatherDesc: [{ value: '无法获取天气' }],
                    humidity: '--',
                    FeelsLikeC: '--'
                }],
                nearest_area: [{ areaName: [{ value: '未知' }] }]
            });
        }
    };

    // 手动刷新天气（重新获取位置）
    const fetchWeather = () => {
        getUserLocation();
    };

    const saveSkinCondition = () => {
        if (!skinCondition.trim()) return;

        const newCondition = {
            id: Date.now(),
            date: currentDate.toISOString(),
            condition: skinCondition,
            weather: weather?.current_condition?.[0] ? {
                temp: weather.current_condition[0].temp_C,
                humidity: weather.current_condition[0].humidity,
                desc: weather.current_condition[0].weatherDesc[0].value
            } : null
        };

        const updated = [newCondition, ...savedConditions].slice(0, 10); // 保留最近10条
        setSavedConditions(updated);
        localStorage.setItem('skinConditions', JSON.stringify(updated));
        setSkinCondition('');
    };

    const deleteSkinCondition = (id) => {
        const updated = savedConditions.filter(item => item.id !== id);
        setSavedConditions(updated);
        localStorage.setItem('skinConditions', JSON.stringify(updated));
    };

    const formatDate = (date) => {
        return new Intl.DateTimeFormat('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'long'
        }).format(date);
    };

    const formatTime = (date) => {
        return new Intl.DateTimeFormat('zh-CN', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        }).format(date);
    };

    const currentCondition = weather?.current_condition?.[0];

    // 根据天气给出护肤建议
    const getWeatherAdvice = () => {
        if (!currentCondition) return '';

        const temp = parseInt(currentCondition.temp_C);
        const humidity = parseInt(currentCondition.humidity);
        const desc = currentCondition.weatherDesc[0].value.toLowerCase();

        let advice = [];

        if (temp > 30) {
            advice.push('🌡️ 高温天气，注意防晒和补水');
        } else if (temp < 10) {
            advice.push('❄️ 气温较低，加强保湿防护');
        }

        if (humidity < 30) {
            advice.push('💧 空气干燥，使用保湿精华');
        } else if (humidity > 80) {
            advice.push('💦 湿度较高，使用清爽型产品');
        }

        if (desc.includes('sun') || desc.includes('clear')) {
            advice.push('☀️ 晴朗天气，务必涂抹防晒');
        }

        return advice.length > 0 ? advice.join('\n') : '天气适宜，正常护肤即可';
    };

    return (
        <div className="space-y-4">
            {/* 日历卡片 */}
            <Card className="p-6">
                <h3 className="text-lg font-semibold mb-3">📅 今日日期</h3>
                {isClient ? (
                    <div className="space-y-2">
                        <p className="text-2xl font-bold">{formatDate(currentDate)}</p>
                        <p className="text-3xl font-bold text-blue-600">{formatTime(currentDate)}</p>
                    </div>
                ) : (
                    <div className="space-y-2">
                        <p className="text-2xl font-bold text-muted-foreground">加载中...</p>
                    </div>
                )}
            </Card>

            {/* 天气卡片 */}
            <Card className="p-6">
                <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-semibold">🌤️ 当前天气</h3>
                    <Button size="sm" variant="ghost" onClick={fetchWeather}>
                        🔄
                    </Button>
                </div>

                {/* 位置信息 */}
                {weather?.nearest_area?.[0] && (
                    <div className="mb-2">
                        <p className="text-xs text-muted-foreground">
                            📍 {weather.nearest_area[0].areaName?.[0]?.value || weather.nearest_area[0].region?.[0]?.value || '当前位置'}
                            {location && ` (${location.latitude.toFixed(2)}, ${location.longitude.toFixed(2)})`}
                        </p>
                    </div>
                )}

                {/* 位置错误提示 */}
                {locationError && (
                    <div className="mb-3 p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded text-xs text-yellow-800 dark:text-yellow-200">
                        ⚠️ {locationError}
                    </div>
                )}

                {currentCondition ? (
                    <div className="space-y-3">
                        <div className="flex items-center gap-4">
                            <div className="text-4xl font-bold text-blue-600">
                                {currentCondition.temp_C}°C
                            </div>
                            <div className="text-sm text-muted-foreground">
                                体感 {currentCondition.FeelsLikeC}°C
                            </div>
                        </div>

                        <div className="space-y-1 text-sm">
                            <p>☁️ {currentCondition.weatherDesc[0].value}</p>
                            <p>💧 湿度: {currentCondition.humidity}%</p>
                        </div>

                        <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                            <p className="text-sm font-semibold mb-2">护肤建议:</p>
                            <p className="text-xs whitespace-pre-line">{getWeatherAdvice()}</p>
                        </div>
                    </div>
                ) : (
                    <div className="text-center text-muted-foreground py-4">
                        <p className="text-sm">正在获取天气信息...</p>
                    </div>
                )}
            </Card>

            {/* 皮肤状况记录 */}
            <Card className="p-6">
                <h3 className="text-lg font-semibold mb-3">📝 皮肤状况记录</h3>

                <div className="space-y-3">
                    <Textarea
                        placeholder="记录今天的皮肤状况... (例如：今天皮肤有点干燥)"
                        value={skinCondition}
                        onChange={(e) => setSkinCondition(e.target.value)}
                        rows={3}
                        className="text-sm"
                    />
                    <Button
                        onClick={saveSkinCondition}
                        className="w-full"
                        size="sm"
                        disabled={!skinCondition.trim()}
                    >
                        💾 保存记录
                    </Button>
                </div>

                {/* 历史记录 */}
                <div className="mt-4 space-y-2 max-h-64 overflow-y-auto">
                    <p className="text-sm font-semibold">最近记录:</p>
                    {savedConditions.length === 0 ? (
                        <p className="text-xs text-muted-foreground text-center py-4">
                            还没有记录
                        </p>
                    ) : (
                        savedConditions.map((item) => (
                            <div
                                key={item.id}
                                className="p-3 bg-muted rounded-lg text-xs space-y-1"
                            >
                                <div className="flex items-start justify-between">
                                    <p className="font-semibold">
                                        {new Date(item.date).toLocaleDateString('zh-CN')}
                                    </p>
                                    <Button
                                        size="sm"
                                        variant="ghost"
                                        className="h-6 w-6 p-0"
                                        onClick={() => deleteSkinCondition(item.id)}
                                    >
                                        ×
                                    </Button>
                                </div>
                                <p>{item.condition}</p>
                                {item.weather && (
                                    <p className="text-muted-foreground">
                                        天气: {item.weather.temp}°C, {item.weather.desc}
                                    </p>
                                )}
                            </div>
                        ))
                    )}
                </div>
            </Card>
        </div>
    );
}
