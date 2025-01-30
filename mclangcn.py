from function import Convert_Lang, crowdin

if __name__ == '__main__':
    pre = True
    crowdin.download_translate(pre)
    Convert_Lang.crowdin_to_mclangcn_csv(pre)
    # Convert_Lang.crowdin_to_mclangcn_csv(pre, 'zh_TW')