import streamlit as st
import random

# Define vocabulary with probabilities
vocabulary = {
    "explore": 0.3, "the": 0.15, "ancient": 0.2, "ruins": 0.1,
    "rest": 0.12, "at": 0.16, "a": 0.14, "quiet": 0.1, "inn": 0.2,
    "climb": 0.18, "towering": 0.2, "mountains": 0.2, "venture": 0.12,
    "into": 0.17, "dense": 0.16, "jungle": 0.14, "follow": 0.12,
    "mysterious": 0.14, "map": 0.13
}

# Define clustering categories
clusters = {
    "explore": "Exploration", "ancient": "Exploration", "ruins": "Exploration",
    "rest": "Relaxation", "quiet": "Relaxation", "inn": "Relaxation",
    "climb": "Exploration", "towering": "Exploration", "mountains": "Exploration",
    "venture": "Adventure", "into": "Adventure", "dense": "Adventure",
    "jungle": "Adventure", "follow": "Adventure", "mysterious": "Adventure",
    "map": "Adventure"
}

# Sampling Methods
def greedy(vocabulary):
    return max(vocabulary, key=vocabulary.get)

def beam(vocabulary):
    top3 = sorted(vocabulary.items(), key=lambda x: x[1], reverse=True)[:3]
    return random.choice([token[0] for token in top3])

def simple_random_sampling(vocabulary):
    tokens, prob = zip(*vocabulary.items())
    return random.choices(tokens, prob)[0]

def top_k_sampling(vocabulary, k=3):
    tokens, prob = zip(*vocabulary.items())
    top_k = sorted(zip(tokens, prob), key=lambda x: x[1], reverse=True)[:k]
    tokens, prob = zip(*top_k)  
    return random.choices(tokens, prob)[0]

def top_p_sampling(vocabulary, p=0.9):
    tokens, prob = zip(*vocabulary.items())
    sorted_items = sorted(zip(tokens, prob), key=lambda x: x[1], reverse=True)
    cumulative_prob = 0.0
    selected_tokens = []
    for token, probability in sorted_items:
        cumulative_prob += probability
        selected_tokens.append(token)
        if cumulative_prob >= p:
            break
    return random.choice(selected_tokens)

def systematic_sampling(vocabulary, n=2):
    tokens = list(vocabulary.keys())
    return tokens[n-1]

def stratified_sampling(vocabulary, categories, num_samples=1):
    selected_tokens = []
    for category in categories:
        category_tokens = [token for token, cat in clusters.items() if cat == category]
        if category_tokens:
            selected_tokens.extend(random.sample(category_tokens, min(len(category_tokens), num_samples)))
    return random.choice(selected_tokens) if selected_tokens else "No valid selection"

def temperature_sampling(vocabulary, temperature):
    tokens = list(vocabulary.keys())
    probabilities = list(vocabulary.values())
    if temperature == 'low':
        adjusted_probs = [pow(prob, 3) for prob in probabilities]  
    elif temperature == 'high':
        adjusted_probs = [pow(prob, 0.3) for prob in probabilities]  
    else:
        adjusted_probs = probabilities
    total_prob = sum(adjusted_probs)
    normalized_probs = [prob / total_prob for prob in adjusted_probs]
    return random.choices(tokens, weights=normalized_probs, k=1)[0]

def cluster_sampling(vocabulary, clusters, num_clusters=2, num_words=3):
    selected_clusters = random.sample(list(set(clusters.values())), num_clusters)
    selected_tokens = [word for word, cat in clusters.items() if cat in selected_clusters]
    if len(selected_tokens) < num_words:
        return "Not enough words available"
    return " ".join(random.sample(selected_tokens, num_words))

def best_of_n_sampling(vocabulary, n=5):
    tokens, prob = zip(*vocabulary.items())
    sampled_tokens = random.choices(tokens, prob, k=n)
    return max(sampled_tokens, key=lambda token: vocabulary[token])

# Streamlit UI
st.title("Token Sampling Simulator")
st.write("Explore different token sampling techniques.")

st.write("The traveler decided to ...")

# Select a sampling technique
sampling_method = st.selectbox("Choose a sampling method:", [
    "Greedy Search", "Beam Search", "Simple Random Sampling",
    "Top-k Sampling", "Top-p Sampling", "Systematic Sampling",
    "Stratified Sampling", "Low Temperature Sampling", "Medium Temperature Sampling",
    "High Temperature Sampling", "Cluster Sampling", "Best of n Sampling"
])

# Additional Parameters
if sampling_method == "Top-k Sampling":
    k = st.slider("Select k value:", 1, 5, 3)
elif sampling_method == "Top-p Sampling":
    p = st.slider("Select p value:", 0.1, 1.0, 0.9)
elif sampling_method == "Stratified Sampling":
    categories = st.multiselect("Choose categories:", ["Exploration", "Relaxation", "Adventure"])
elif sampling_method in ["Low Temperature Sampling", "Medium Temperature Sampling", "High Temperature Sampling"]:
    temp = sampling_method.split()[0].lower()
elif sampling_method == "Best of n Sampling":
    n = st.slider("Select n value:", 1, 10, 5)

# Run Simulation
if st.button("Simulate"):
    if sampling_method == "Greedy Search":
        result = greedy(vocabulary)
    elif sampling_method == "Beam Search":
        result = beam(vocabulary)
    elif sampling_method == "Simple Random Sampling":
        result = simple_random_sampling(vocabulary)
    elif sampling_method == "Top-k Sampling":
        result = top_k_sampling(vocabulary, k)
    elif sampling_method == "Top-p Sampling":
        result = top_p_sampling(vocabulary, p)
    elif sampling_method == "Systematic Sampling":
        result = systematic_sampling(vocabulary)
    elif sampling_method == "Stratified Sampling":
        result = stratified_sampling(vocabulary, categories)
    elif sampling_method in ["Low Temperature Sampling", "Medium Temperature Sampling", "High Temperature Sampling"]:
        result = temperature_sampling(vocabulary, temp)
    elif sampling_method == "Cluster Sampling":
        result = cluster_sampling(vocabulary, clusters)
    elif sampling_method == "Best of n Sampling":
        result = best_of_n_sampling(vocabulary, n)

    st.write(f"The traveler decided to **{result}**")

