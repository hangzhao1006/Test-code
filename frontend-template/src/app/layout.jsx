import './globals.css';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import ClientProviders from '@/components/ClientProviders';

export const metadata = {
    title: 'SkinMe - AI Skincare Assistant',
    description: 'AI-powered skincare analysis and product recommendations',
}

export default function RootLayout({ children }) {
    return (
        <html lang="en" className="h-full" suppressHydrationWarning>
            <head>
                <link href="assets/logo.svg" rel="shortcut icon" type="image/x-icon"></link>
            </head>
            <body className="flex flex-col min-h-screen">
                <ClientProviders>
                    <Header />
                    <main className="flex-grow pt-16">{children}</main>
                    <Footer />
                </ClientProviders>
            </body>
        </html>
    );
}