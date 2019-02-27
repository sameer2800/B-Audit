package com.credits.baudit.contracts;


import java.util.Date;
import java.util.HashSet;
import java.util.Set;

public class House {

	private final String name ;
	private final Address owner;
	private final long wallet;
	private final Date constructionDate;
	private final String builderName;
	private final Set<Device> devices;
	
	public House(String name, Address owner,long wallet, Date constructionDate, String builderName) {
		this.name = name;
		this.owner = owner;
		this.wallet = wallet;
		//this.owner = msg.sender;
		//this.wallet =msg.value;
		this.constructionDate = constructionDate;
		this.builderName = builderName;
		devices = new HashSet<Device>();
	}
	
	public void registerDevice(Device device) {
		//require(msg.sender, this.owner); 
		devices.add(device);
	}
	
	public void deRegisterDevice(Device device) {
		//require(msg.sender, this.owner); 
		devices.remove(device);
	}
	
	public Set<Device> getDevices() {
		return devices;
	}


	public String getName() {
		return name;
	}

	public Date getConstructionDate() {
		return constructionDate;
	}

	public String getBuilderName() {
		return builderName;
	}
	
	
}
