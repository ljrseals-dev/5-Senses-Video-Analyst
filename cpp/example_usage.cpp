// Minimal C++20 example showing how to embed and print the 5-Senses master prompt.
// Build:  g++ -std=c++20 -O2 example_usage.cpp -o example_usage
// Or with CMake (see CMakeLists.txt).

#include "5_senses_prompt.hpp"

#include <iostream>
#include <string_view>

int main() {
    using namespace five_senses;

    std::cout << "Agent : " << kAgentName << '\n'
              << "Model : " << kRecommendedOllamaModel << "\n\n"
              << "----- SYSTEM PROMPT (first 400 chars) -----\n"
              << kMasterPrompt.substr(0, 400) << "...\n\n"
              << "Total prompt length: " << kMasterPrompt.size() << " characters\n";

    // In a real host you would pass kMasterPrompt as the "system" role
    // message to your local OpenAI-compatible endpoint, e.g.:
    //
    //   curl http://localhost:11434/api/chat -d '{
    //     "model": "qwen2.5vl:3b",
    //     "messages": [
    //       {"role": "system", "content": "<contents of kMasterPrompt>"},
    //       {"role": "user",   "content": "Analyse https://..."}
    //     ]
    //   }'

    return 0;
}
