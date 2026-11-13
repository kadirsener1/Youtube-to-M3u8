import os
import yt_dlp

def get_stream_url(youtube_url):
    ydl_opts = {
        'cookiefile': 'cookies.txt',  # GitHub Secrets'tan gelen çerez dosyası
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            
            # Eğer canlı yayınsa doğrudan m3u8/manifest adresini al
            if 'url' in info:
                return info['url']
            
            # Alternatif formatlar içinden bulma
            formats = info.get('formats', [])
            for f in formats:
                if f.get('protocol') in ['m3u8_native', 'm3u8'] or 'm3u8' in f.get('format_id', ''):
                    return f.get('url')
                    
            # Hiçbiri bulunamazsa son çare info['url']
            return info.get('url')
    except Exception as e:
        print(f"⚠️ Hata ({youtube_url}): {e}")
        return None

def main():
    print("📡 Playlist güncelleme başlatılıyor...")
    
    # Örnek kanal listesi (Kendi kanal okuma mantığına göre uyarlayabilirsin)
    channels = [
        {"name": "Akit TV", "url": "https://www.youtube.com/watch?v=N9SMoh8gLJI"},
        # Diğer kanalların buraya gelebilir
    ]
    
    playlist_lines = ["#EXTM3U\n"]
    
    for ch in channels:
        print(f"📺 İşleniyor: {ch['name']}")
        stream_url = get_stream_url(ch['url'])
        
        if stream_url:
            playlist_lines.append(f"#EXTINF:-1,{ch['name']}\n{stream_url}\n")
            print(f"  ✅ Başarılı: {stream_url[:50]}...")
        else:
            print(f"  ❌ Yayın alınamadı: {ch['name']}")
            
    # streams.m3u8 dosyasına kaydetme
    with open("streams.m3u8", "w", encoding="utf-8") as f:
        f.writelines(playlist_lines)
        
    print("✨ Tüm işlemler tamamlandı!")

if __name__ == "__main__":
    main()
