<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import axios from 'axios';
defineEmits(['close'])
const props = defineProps(['details'])
// Watch for changes in the details prop
watch(() => props.details, (newDetails, oldDetails) => {
}, { deep: true }); // Add deep: true

function getIcon(details){
    if(details == "..."){
        return "/loading.svg"
    }else{
        return "/question.svg"
    }
}
</script>

<template>
<div class="bg-white rounded-xl w-1/2 h-1/2 shadow-xl overflow-y-auto p-4 flex-1 relative mr-10 ml-10">
    <button @click="$emit('close')" class="absolute top-0 right-0 w-[1.5em] mr-4 mt-4">
        <img src="/close.svg" />
    </button>
    <div class="flex h-[1.5em]"></div>
    <h1 class="text-center font-semibold text-xl">{{ details?.name }}</h1>
        <!-- <div v-for="(value, key) in details" :key="key" class="mb-3">
            <p class="text-gray-800">
                <span class="font-medium capitalize">{{ key }}:</span>
                {{ value }}
            </p>
        </div>    -->
    <div class="flex justify-center items-center h-full">
        <img class="w-1/2 h-1/2" :src="getIcon(details)" />
    </div>
    
</div>

</template>


<style>
</style>