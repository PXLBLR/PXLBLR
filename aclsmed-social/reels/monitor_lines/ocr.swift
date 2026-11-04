// OCR with macOS Vision: prints one JSON line per image, {"file":..., "lines":[[text, x, y, w, h], ...]}
// (normalized boxes, origin top-left).   swift ocr.swift a.png b.png ...
import Foundation
import Vision
import AppKit

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("{\"file\":\"\(path)\",\"error\":\"unreadable\"}"); continue
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    try? VNImageRequestHandler(cgImage: cg).perform([req])
    var lines: [[Any]] = []
    for o in req.results ?? [] {
        guard let t = o.topCandidates(1).first?.string else { continue }
        let b = o.boundingBox
        lines.append([t, b.minX, 1 - b.maxY, b.width, b.height])
    }
    let data = try! JSONSerialization.data(withJSONObject: ["file": path, "lines": lines])
    print(String(data: data, encoding: .utf8)!)
}
