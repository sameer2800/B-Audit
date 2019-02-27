package com.credits.baudit.contracts;

import java.util.ArrayList;

public class Auction {
	
	private String id;
	private Device device;
	private long basePrice;
	private boolean status; 
	private ArrayList<AuctionBid>auctionBids;
	
	public Auction(String id, Device device, long basePrice) {
		super();
		this.setId(id);
		this.device = device;
		this.basePrice = basePrice;
		this.setStatus(true);
		this.auctionBids = new ArrayList<AuctionBid>();
	}
	
	public void  addBid(AuctionBid auctionBid) {
		auctionBids.add(auctionBid);
	}
	
	public ArrayList<AuctionBid> getAuctionBids() {
		return auctionBids;
	}
	
	public Device getDevice() {
		return device;
	}
	public void setDevice(Device device) {
		this.device = device;
	}
	public long getBasePrice() {
		return basePrice;
	}
	public void setBasePrice(long basePrice) {
		this.basePrice = basePrice;
	}
	public boolean isStatus() {
		return status;
	}
	public void setStatus(boolean status) {
		this.status = status;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}
	
	
}
